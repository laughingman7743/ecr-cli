# -*- coding: utf-8 -*-
from __future__ import absolute_import


class EcrConfig(object):

    def __init__(self, tags, profile_name=None, region_name=None, registry_id=None):
        self.tags = tags
        self.profile_name = profile_name
        self.region_name = region_name
        self.registry_id = registry_id

    @staticmethod
    def from_dict(value):
        tags = value.get('tags', None)
        assert tags, 'Missing sequence `tags`.'
        return EcrConfig(
            tags,
            value.get('profile_name', None),
            value.get('region_name', None),
            value.get('registry_id', None),)

    def _key(self):
        return (self.tags,
                self.profile_name,
                self.region_name,
                self.registry_id,)

    def __repr__(self):
        return 'EcrConfig{0}'.format(self._key())
