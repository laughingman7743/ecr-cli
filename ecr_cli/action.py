# -*- coding: utf-8 -*-
from __future__ import absolute_import

import itertools
import logging
import sys

import click
import docker
from docker.errors import DockerException
from docker.utils.json_stream import json_stream
from future.utils import string_types
from tqdm import tqdm

from ecr_cli.client import EcrClient

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler(sys.stdout))
_logger.setLevel(logging.INFO)


class EcrAction(object):

    def __init__(self, profile_name=None, region_name=None, registry_id=None,
                 debug=False):
        if debug:
            _logger.setLevel(logging.DEBUG)
        self._docker_client = docker.from_env()
        self._ecr_client = EcrClient(profile_name, region_name)
        self._registry_id = registry_id
        self._registry = None
        self.login()
        assert self._registry, 'Docker registry is missing.'

    def login(self, reauth=True):
        username, password, registry = self._ecr_client.get_authorization_token(
            self._registry_id)
        self._registry = registry.replace('https://', '')
        self._docker_client.login(username=username, password=password,
                                  registry=self._registry, reauth=reauth)
        _logger.debug(self._registry)
        return self._registry

    def _process_stream(self, stream):
        result_stream, internal_stream = itertools.tee(json_stream(stream))
        image_ids = set()
        progress_bars = {}
        for chunk in internal_stream:
            _logger.debug(chunk)
            if 'error' in chunk:
                raise DockerException(chunk['error'], result_stream)
            elif 'status' in chunk:
                status = chunk['status']
                id = chunk.get('id', None)
                if status in ['Downloading', 'Extracting', 'Pushing']:
                    current = chunk['progressDetail']['current']
                    total = chunk['progressDetail']['total']
                    if id in progress_bars:
                        bar, prev_current, total = progress_bars[id]
                        update = current - prev_current
                        bar.update(1 if total < current else update)
                        bar.set_description_str('{0}: {1}'.format(id, status))
                    else:
                        bar = tqdm(desc='{0}: {1}'.format(id, status),
                                   total=total,
                                   unit='B', unit_scale=True, unit_divisor=1024,
                                   position=len(progress_bars))
                        bar.update(current)
                    progress_bars.update({id: (bar, current, total)})
                elif status in ['Verifying Checksum']:
                    bar, prev_current, total = progress_bars[id]
                    update = bar.total - prev_current
                    bar.update(1 if update < 0 else update)
                    bar.set_description_str('{0}: {1}'.format(id, status))
                elif status in ['Download complete']:
                    bar, prev_current, total = progress_bars[id]
                    bar.clear()  # TODO Progress bar can not be reset
                    progress_bars.update({id: (bar, 0, total)})
                    bar.set_description_str('{0}: {1}'.format(id, status))
                elif status in ['Pull complete', 'Pushed']:
                    bar, prev_current, total = progress_bars[id]
                    update = bar.total - prev_current
                    bar.update(1 if update < 0 else update)
                    bar.set_description_str('{0}: {1}'.format(id, status))
                else:
                    if 'id' in chunk:
                        click.echo('{0}: {1}'.format(id, status))
                    else:
                        click.echo(status)
            elif 'aux' in chunk:
                aux = chunk['aux']
                if 'Digest' in aux:
                    image_ids.add(aux['Digest'])
                elif 'ID' in aux:
                    image_ids.add(aux['ID'])
            elif 'stream' in chunk:
                click.echo(chunk['stream'].strip('\n'))
            else:
                click.echo(chunk)
        for bar, _, _ in progress_bars.values():
            bar.close()
        return tuple(image_ids)

    def build(self, tags, path=None, dockerfile=None, cache=True, rm=False,
              force_rm=False, pull=False, squash=False, quiet=False):
        tag = '{0}/{1}'.format(self._registry, tags[0])
        resp = self._docker_client.images.client.api.build(
            path=path, tag=tag, dockerfile=dockerfile, nocache=not cache,
            rm=rm, forcerm=force_rm, pull=pull, squash=squash, quiet=quiet)
        if isinstance(resp, string_types):
            image_id = resp
        else:
            image_ids = self._process_stream(resp)
            if not image_ids:
                image_id = tag
            else:
                image_id = image_ids[0]
        image = self._docker_client.images.get(image_id)
        if tags and len(tags) > 1:
            for t in tags[1:]:
                name, tag = tuple(t.split(':'))
                image.tag('{0}/{1}'.format(self._registry, name), tag, force=True)
        return image

    def push(self, name, tag=None):
        resp = self._docker_client.images.push(
            '{0}/{1}'.format(self._registry, name), tag, stream=True)
        image_ids = self._process_stream(resp)
        return tuple(image_ids)

    def pull(self, name, tag=None):
        resp = self._docker_client.images.client.api.pull(
            '{0}/{1}'.format(self._registry, name), tag, stream=True)
        self._process_stream(resp)
