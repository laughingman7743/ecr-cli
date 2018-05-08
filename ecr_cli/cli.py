#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import click

import ecr_cli.message as msg
from ecr_cli import CONTEXT_SETTINGS
from ecr_cli.action import EcrAction
from ecr_cli.util import load_ecr_config


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--profile', type=str, required=False,
              help=msg.HELP_OPTION_PROFILE)
@click.option('--region', type=str, required=False,
              help=msg.HELP_OPTION_REGION)
@click.option('--registry-id', type=str, required=False,
              help=msg.HELP_OPTION_REGISTRY_ID)
@click.option('--debug/--no-debug', required=False, default=False,
              help=msg.HELP_OPTION_DEBUG)
@click.pass_context
def cli(ctx, profile, region, registry_id, debug):
    ctx.obj = dict()
    ctx.obj['profile'] = profile
    ctx.obj['region'] = region
    ctx.obj['registry_id'] = registry_id
    ctx.obj['debug'] = debug


@cli.command(help=msg.HELP_COMMAND_BUILD)
@click.argument('path', type=click.Path(exists=True, dir_okay=True), nargs=1, required=True)
@click.option('--tag', '-t', type=str, multiple=True, required=False,
              help=msg.HELP_OPTION_TAG)
@click.option('--dockerfile', type=click.Path(exists=True, file_okay=True), required=False,
              help=msg.HELP_OPTION_DOCKERFILE)
@click.option('--configfile', type=click.Path(exists=True, file_okay=True), required=False,
              help=msg.HELP_OPTION_CONFIGFILE)
@click.option('--cache/--no-cache', default=True, required=False,
              help=msg.HELP_OPTION_CACHE)
@click.option('--rm/--no-rm', default=False, required=False,
              help=msg.HELP_OPTION_RM)
@click.option('--force-rm/--no-force-rm', default=False, required=False,
              help=msg.HELP_OPTION_FORCE_RM)
@click.option('--pull/--no-pull', default=False, required=False,
              help=msg.HELP_OPTION_PULL)
@click.option('--squash/--no-squash', default=False, required=False,
              help=msg.HELP_OPTION_SQUASH)
@click.option('--push/--no-push', default=False, required=False,
              help=msg.HELP_OPTION_PUSH)
@click.option('--quiet/--no-quiet', default=False, required=False,
              help=msg.HELP_OPTION_QUIET)
@click.option('--no-profile', is_flag=True, default=False, required=False,
              help=msg.HELP_OPTION_NO_PROFILE)
@click.pass_context
def build(ctx, path, tag, dockerfile, configfile, cache, rm, force_rm,
          pull, squash, push, quiet, no_profile):
    if not configfile:
        configfile = os.path.join(os.path.dirname(dockerfile) if dockerfile else path,
                                  '.ecr.yml')
    config = load_ecr_config(configfile)
    if not config and not tag:
        raise RuntimeError('Missing argument `tag`.')

    action = EcrAction(
        profile_name=None if no_profile else
        ctx.obj['profile'] if ctx.obj['profile'] else config.profile_name,
        region_name=ctx.obj['region'] if ctx.obj['region'] else config.region_name,
        registry_id=ctx.obj['registry_id'] if ctx.obj['registry_id'] else config.registry_id,
        debug=ctx.obj['debug'])
    action.build(tag if tag else config.tags,
                 path=path, dockerfile=dockerfile, cache=cache, rm=rm, force_rm=force_rm,
                 pull=pull, squash=squash, quiet=quiet)
    if push:
        for t in config.tags:
            action.push(t)


@cli.command(help=msg.HELP_COMMAND_PUSH)
@click.argument('name', type=str, nargs=-1, required=True)
@click.pass_context
def push(ctx, name):
    action = EcrAction(profile_name=ctx.obj['profile'],
                       region_name=ctx.obj['region'],
                       registry_id=ctx.obj['registry_id'],
                       debug=ctx.obj['debug'])
    for n in name:
        action.push(n)


@cli.command(help=msg.HELP_COMMAND_PULL)
@click.argument('name', type=str, nargs=-1, required=True)
@click.pass_context
def pull(ctx, name):
    action = EcrAction(profile_name=ctx.obj['profile'],
                       region_name=ctx.obj['region'],
                       registry_id=ctx.obj['registry_id'],
                       debug=ctx.obj['debug'])
    for n in name:
        action.pull(n)


if __name__ == '__main__':
    cli()
