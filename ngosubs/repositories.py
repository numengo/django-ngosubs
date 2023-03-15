# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from io import BytesIO
from django.contrib.auth.models import Group
from future.utils import with_metaclass
from ngoschema.protocols import ObjectProtocol, SchemaMetaclass
from ngoschema.protocols.repository import Repository
from ngoutils.repositories import DjangoModelNodeRepository, django_model_node_repositories_registry
from ngoutils.managers.model_builder import DjangoModelBuilder, django_model_builder
from ngomm.models import Node
from ngomm_cms import settings as mm_cms_settings
from ngomm_cms.models import GroupNode, SubscriptionPlanNode, SubscriptionPlanSetNode

#from .models import DjangoGroupNode, DjangoSubscriptionPlanNode, DjangoSubscriptionPlanSetNode


#@django_model_node_repositories_registry.register()
#class GroupRepository(with_metaclass(SchemaMetaclass, DjangoModelNodeRepository)):
#    instanceClass = Group
#    _django_model_node = DjangoGroupNode
#
#
#@django_model_node_repositories_registry.register()
#class SubscriptionPlanRepository(with_metaclass(SchemaMetaclass, DjangoModelNodeRepository)):
#    instanceClass = SubscriptionPlanNode
#    _django_model_node = DjangoSubscriptionPlanNode
#
#    def __init__(self, *args, **kwargs):
#        from django.conf import settings as django_settings
#        DjangoModelNodeRepository.__init__(self, *args, **kwargs)
#        self._languages = [lt[0] for lt in django_settings.LANGUAGES]
#
#    def for_db(self, object_node):
#        ret = {'plan_name': object_node.name,
#               'slug': object_node.slug,
#               'grace_period': None,
#               'group': None}
#        return ret
#
#
#@django_model_node_repositories_registry.register()
#class SubscriptionPlanSetRepository(with_metaclass(SchemaMetaclass, DjangoModelNodeRepository)):
#    instanceClass = SubscriptionPlanSetNode
#    _django_model_node = DjangoSubscriptionPlanSetNode
#
#    def __init__(self, *args, **kwargs):
#        from django.conf import settings as django_settings
#        DjangoModelNodeRepository.__init__(self, *args, **kwargs)
#        self._languages = [lt[0] for lt in django_settings.LANGUAGES]
#        self._plan_repo = SubscriptionPlanRepository(session=self._session)
#
#    @property
#    def plan_repo(self):
#        return self._plan_repo
#
#    def for_db(self, object_node):
#        ret = object_node.do_serialize(add_identity_keys=False)
#        return ret
#
#    def create_or_update_db(self, object_node, **opts):
#        object_node._logger.info("%s Processing '%s'", object_node, object_node.identityKeys)
#        node_id = str(object_node.node.ID)
#        node_lm = int(object_node.node.MODIFIED)
#        django_model_node = self.djangoModelNode
#        object_node_class = object_node.__class__
#        model = django_model_node._django_model
#        mk = django_model_node._model_key
#
#        for p in object_node.plans:
#            self.plan_repo.create_or_update_db(p)
#
#        self.register(object_node)
#        on_db = self.get_db(object_node)
#        session = self._session
#        if not on_db:
#            dmn_data = self.for_db(object_node)
#            #json_data = object_node.do_serialize(add_identity_keys=False)
#            #dmn_data = dict(json_data)
#            for k, rl in object_node._relationships.items():
#                fk = rl._foreignKey
#                fc = rl._foreignClass
#                if fk in dmn_data:
#                    fkv = dmn_data[rl._foreignKey]
#                    for rp in session.repositories:
#                        if isinstance(rp, DjangoModelNodeRepository) and issubclass(rp._django_model_node._object_node, rl._foreignClass):
#                            on = rp.get_instance(fkv)
#                            don = rp.get_db(on)
#                            dmn_data[fk] = don.djangoObject
#            try:
#                on_db = model.objects.create(**dmn_data)
#                dmn = dict(node_id=node_id, last_modified=node_lm, json_data=json_data, **{mk: on_db})
#                dmn_db = django_model_node.objects.create(**dmn)
#                object_node._logger.info("%s Created %s DB[%i]", object_node, model, on_db.id)
#            except Exception as er:
#                if on_db:
#                    on_db.delete()
#        else:
#            pass
#        return on_db
#
