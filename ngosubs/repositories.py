# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from io import BytesIO
from django.contrib.auth.models import Group
from future.utils import with_metaclass
from ngoschema.protocols import ObjectProtocol, SchemaMetaclass
from ngoschema.protocols.repository import Repository
from ngoutils.repositories import DjangoModelNodeRepository, django_model_node_repository_registry
from ngomm.models import Node
from ngomm_cms import settings as mm_cms_settings
from ngomm_cms.models import GroupNode, SubscriptionPlanNode, SubscriptionPlanSetNode

from .models import DjangoGroupNode, DjangoSubscriptionPlanNode, DjangoSubscriptionPlanSetNode


@django_model_node_repository_registry.register()
class GroupRepository(with_metaclass(SchemaMetaclass, DjangoModelNodeRepository)):
    instanceClass = Group
    _django_model_node = DjangoGroupNode


@django_model_node_repository_registry.register()
class SubscriptionPlanRepository(with_metaclass(SchemaMetaclass, DjangoModelNodeRepository)):
    instanceClass = SubscriptionPlanNode
    _django_model_node = DjangoSubscriptionPlanNode

    def __init__(self, *args, **kwargs):
        from django.conf import settings as django_settings
        DjangoModelNodeRepository.__init__(self, *args, **kwargs)
        self._languages = [lt[0] for lt in django_settings.LANGUAGES]

    def for_db(self, object_node):
        ret = {'plan_name': object_node.name,
               'slug': object_node.slug,
               'grace_period': None,
               'group': None}
        json_data = object_node.do_serialize(add_identity_keys=False)
        return dict(json_data)

    def create_or_update_dbXXXX(self, plan, parent_db=None):
        plan._logger.info(u"%s Processing '%s'", plan, plan.title)
        node_id = str(plan.node.ID)
        node_lm = str(plan.node.MODIFIED)
        self.register(plan)
        pn_db = self.get_db(plan)
        session = self._session
        if not pn_db:
            data = plan.for_cms()
            language = data.pop('language', None) or self._languages[0]
            title = data.pop('title', None) or page.title
            template = data.pop('template', None)
            db_page = create_page(title, template, language, parent=parent_db, **data)
            pn_db = DjangoPageNode.objects.create(node_id=node_id, last_modified=node_lm, page=db_page)
            db_title = db_page.get_title_obj(language)
            tn = DjangoTitleNode.objects.create(node_id=node_id, last_modified=node_lm, title=db_title)
            page._logger.info(u"%s Created Page DB[%i]", page, db_page.id)
            page._logger.info(u"%s Created Title DB[%i]", page, db_title.id)
            meta = page.for_meta()
            image = None
            if page.og_image:
                in_ = self.title_repo.plugin_repo.image_repo.create_or_update_db(page.image_plugin)
                image = in_.file
            meta_db = PageMeta.objects.create(extended_object= db_page, image=image, **meta)
            page._logger.info(u"%s Created PageMeta DB[%i]", page, meta_db.id)
            sitemap = page.for_sitemap()
            sitemap_db = PageSitemapProperties.objects.create(extended_object=db_page, **sitemap)
            page._logger.info(u"%s Created TitleMeta DB[%i]", page, sitemap_db.id)
        else:
            db_page = pn_db.page
            if node_lm != pn_db.last_modified:
                data_page = page.for_cms_page()
                db_page.update(refresh=True, draft_only=False, **data_page)
                db_page.save()
                meta_db = PageMeta.objects.get(extended_object=db_page)
                for k, v in page.for_meta().items():
                    setattr(meta_db, k, v)
                meta_db.save()
                sitemap_db = PageSitemapProperties.objects.get(extended_object=db_page)
                for k, v in page.for_sitemap().items():
                    setattr(sitemap_db, k, v)
                sitemap_db.save()
                pn_db.last_modified = node_lm
                pn_db.save()
                page._logger.info(u"%s Updated Page DB[%i]", page, db_page.id)
        self._title_repo.create_or_update_db(page, parent_db=db_page)
        for t in page.translations:
            if t.language in self._languages:
                self.title_repo.create_or_update_db(t, parent_db=db_page)
        for p in page.subpages:
            self.create_or_update_db(p, parent_db=db_page)
        return pn_db


@django_model_node_repository_registry.register()
class SubscriptionPlanSetRepository(with_metaclass(SchemaMetaclass, DjangoModelNodeRepository)):
    instanceClass = SubscriptionPlanSetNode
    _django_model_node = DjangoSubscriptionPlanSetNode

    def __init__(self, *args, **kwargs):
        from django.conf import settings as django_settings
        DjangoModelNodeRepository.__init__(self, *args, **kwargs)
        self._languages = [lt[0] for lt in django_settings.LANGUAGES]
        self._plan_repo = SubscriptionPlanRepository(session=self._session)

    @property
    def plan_repo(self):
        return self._plan_repo

    def for_db(self, object_node):
        json_data = object_node.do_serialize(add_identity_keys=False)
        return dict(json_data)

    def create_or_update_dbXXX(self, planset, parent_db=None):
        planset._logger.info(u"%s Processing '%s'", planset, planset.name)
        node_id = str(planset.node.ID)
        node_lm = str(planset.node.MODIFIED)
        self.register(planset)
        data = planset.do_serialize()
        language = data.pop('language', planset.language) or parent_db.languages
        published = data.pop('published', None)
        pn = self.get_db(planset)
        if not pn:
            pn = data.pop('title', planset.title)
            db_title = create_title(language, title, page=parent_db, parent=parent_db.parent_page, **data)
            tn = DjangoTitleNode.objects.create(node_id=node_id, last_modified=node_lm, title=db_title)
            translation._logger.info(u"%s Created Title DB[%i]", translation, db_title.id)
            meta = translation.for_meta()
            image = None
            if translation.og_image:
                in_ = self.plugin_repo.image_repo.create_or_update_db(translation.image_plugin)
                image = in_.file
            meta_db = TitleMeta.objects.create(extended_object= db_title, image=image, **meta)
            translation._logger.info(u"%s Created TitleMeta DB[%i]", translation, meta_db.id)
        else:
            db_title = tn.title
            if node_lm != tn.last_modified:
                for k, v in data.items():
                    setattr(db_title, k, v)
                db_title.save()
                meta_db = TitleMeta.objects.get(extended_object=db_title)
                for k, v in translation.for_meta().items():
                    setattr(meta_db, k, v)
                meta_db.save()
                tn.last_modified = node_lm
                tn.save()
                translation._logger.info(u"%s Updated Title DB[%i]", translation, db_title.id)
        for ph in translation.placeholders:
            self.plugin_repo.create_or_update_db(ph, str(ph.slot), language, db_title)
            #for pl in ph.plugins:
            #    self.plugin_repo.create_or_update_db(pl, str(ph.slot), language, db_title)
        if published:
            translation._logger.info(u"%s Publishing [%i]", translation, db_title.id)
            parent_db.publish(language)
        return tn
