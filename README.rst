.. image:: https://img.shields.io/pypi/pyversions/ecr-cli.svg
    :target: https://pypi.org/project/ecr-cli/

.. image:: https://travis-ci.org/laughingman7743/ecr-cli.svg?branch=master
    :target: https://travis-ci.org/laughingman7743/ecr-cli

.. image:: https://codecov.io/gh/laughingman7743/ecr-cli/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/laughingman7743/ecr-cli

.. image:: https://img.shields.io/pypi/l/ecr-cli.svg
    :target: https://github.com/laughingman7743/ecr-cli/blob/master/LICENSE


ecr-cli
=======

Goodbye docker login & a long registry URL for `Amazon ECR`_ :)

.. _`Amazon ECR`: https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html

Requirements
------------

* Python

  - CPython 2,7, 3,4, 3.5, 3.6

* Docker

  - API version >= 1.21

Installation
------------

.. code:: bash

    $ pip install ecr-cli

ECR Configuration file
----------------------

If you place a file in `YAML format`_ with the filename ``.ecr.yml`` in the same directory as ``Dockerfile``,
profile name, region name, registry ID and tag can be set.

.. _`YAML format`: http://www.yaml.org/

+--------------+------------+-------------------------------------------------------------------------------------+
| Key name     | Value      | Description                                                                         |
+==============+============+=====================================================================================+
| profile_name | str        | Use a specific profile from your credential file.                                   |
+--------------+------------+-------------------------------------------------------------------------------------+
| region_name  | str        | The region to use. Overrides config/env settings.                                   |
+--------------+------------+-------------------------------------------------------------------------------------+
| registry_id  | int        | AWS account ID that correspond to a Amazon ECR registry that you want to log in to. |
+--------------+------------+-------------------------------------------------------------------------------------+
| tags         | seq of str | Name and optionally a tag in the ‘name:tag’ format.                                 |
+--------------+------------+-------------------------------------------------------------------------------------+

``.ecr.yml`` example:

.. code:: yaml

    profile_name: null
    region_name: us-west-2
    registry_id: null
    tags:
      - java/amazonlinux-oracle-java:latest
      - java/amazonlinux-oracle-java:2017.12-8u162

NOTE: Command line options override settings in this file.

Usage
-----

.. code::

    Usage: ecr [OPTIONS] COMMAND [ARGS]...

    Options:
      --profile TEXT         Use a specific profile from your credential file.
      --region TEXT          The region to use. Overrides config/env settings.
      --registry-id INTEGER  AWS account ID that correspond to a Amazon ECR registry that you want to log in to.
      --debug / --no-debug   Turn on debug logging.
      -h, --help             Show this message and exit.

    Commands:
      build  Build an image from a Dockerfile.
      pull   Pull an image or a repository from a Amazon ECR registry
      push   Push an image or a repository to a Amazon ECR registry.

Build
~~~~~

.. code::

    Usage: ecr build [OPTIONS] PATH

      Build an image from a Dockerfile.

    Options:
      -t, --tag TEXT              Name and optionally a tag in the `name:tag` format.
      --dockerfile PATH           Name of the Dockerfile (Default is `PATH/Dockerfile`).
      --configfile PATH           Name of the ECR configuration file (Default is `PATH/.ecr.yml`).
      --cache / --no-cache        Use cache when building the image.
      --rm / --no-rm              Remove intermediate containers after a successful build.
      --force-rm / --no-force-rm  Always remove intermediate containers.
      --pull / --no-pull          Always attempt to pull a newer version of the image.
      --squash / --no-squash      Squash newly built layers into a single new layer.
      --push / --no-push          Push an image or a repository to a Amazon ECR registry after a successful build.
      --quiet / --no-quiet        Suppress the standard output.
      --no-profile                Forcibly disable the ECR configuration file profile.
      -h, --help                  Show this message and exit.

Push
~~~~

.. code::

    Usage: ecr push [OPTIONS] NAME...

      Push an image or a repository to a Amazon ECR registry.

    Options:
      --quiet / --no-quiet        Suppress the standard output.
      -h, --help  Show this message and exit.

Pull
~~~~

.. code::

    Usage: ecr pull [OPTIONS] NAME...

      Pull an image or a repository from a Amazon ECR registry

    Options:
      --quiet / --no-quiet        Suppress the standard output.
      -h, --help  Show this message and exit.

Authentication
--------------

Support `Boto3 credentials`_.

.. _`Boto3 credentials`: http://boto3.readthedocs.io/en/latest/guide/configuration.html

Testing
-------

TODO

TODO
----

#. Progress bar can not be reset :(
#. Vacuum command
#. Tests
