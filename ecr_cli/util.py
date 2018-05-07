# -*- coding: utf-8 -*-
from __future__ import absolute_import

import codecs
import os

import yaml

from ecr_cli.model import EcrConfig


def load_ecr_config(file_):
    config = None
    if os.path.exists(file_):
        with codecs.open(file_, 'rb', 'utf-8') as f:
            config = EcrConfig.from_dict(yaml.load(f))
    return config
