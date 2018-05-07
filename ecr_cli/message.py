# -*- coding: utf-8 -*-
from __future__ import absolute_import

HELP_COMMAND_BUILD = 'Build an image from a Dockerfile.'
HELP_COMMAND_PUSH = 'Push an image or a repository to a Amazon ECR registry.'
HELP_COMMAND_PULL = 'Pull an image or a repository from a Amazon ECR registry'

HELP_OPTION_PROFILE = 'Use a specific profile from your credential file.'
HELP_OPTION_REGION = 'The region to use. Overrides config/env settings.'
HELP_OPTION_DEBUG = 'Turn on debug logging.'
HELP_OPTION_REGISTRY_ID = 'AWS account ID that correspond to a Amazon ECR registry ' \
                          'that you want to log in to.'
HELP_OPTION_TAG = 'Name and optionally a tag in the `name:tag` format.'
HELP_OPTION_DOCKERFILE = 'Name of the Dockerfile (Default is `PATH/Dockerfile`).'
HELP_OPTION_CONFIGFILE = 'Name of the ECR configuration file (Default is `PATH/.ecr.yml`).'
HELP_OPTION_CACHE = 'Use cache when building the image.'
HELP_OPTION_RM = 'Remove intermediate containers after a successful build.'
HELP_OPTION_FORCE_RM = 'Always remove intermediate containers.'
HELP_OPTION_PULL = 'Always attempt to pull a newer version of the image.'
HELP_OPTION_SQUASH = 'Squash newly built layers into a single new layer.'
HELP_OPTION_PUSH = 'Push an image or a repository to a Amazon ECR registry ' \
                   'after a successful build.'
HELP_OPTION_QUIET = 'Suppress the build output and print image ID on success.'
HELP_OPTION_NO_PROFILE = 'Forcibly disable the ECR configuration file profile.'
