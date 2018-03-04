# -*- coding: utf-8 -*-
from __future__ import absolute_import
import codecs
import os

import yaml

from ecr_cli.model import EcrConfig


def load_config(path):
    conf = os.path.join(path, '.ecr.yml')
    config = None
    if os.path.exists(conf):
        with codecs.open(conf, 'rb', 'utf-8') as f:
            config = EcrConfig.from_dict(yaml.load(f))
    return config
