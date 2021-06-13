# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 12:46:34 2015

@author: Cedric
"""
import logging
import time
from django.core.management.base import BaseCommand
from ngoschema.session import default_session
from ngomm.converters import Freeplane2InstanceTransform
from ngocms.repositories import PageRepository
from ngomm.models import Map
from ngosubs.nodes import SubscriptionsNode, SubscriptionPlanSetNode, SubscriptionPlanNode
from ngosubs.repositories import SubscriptionPlanRepository, SubscriptionPlanSetRepository


class Command(BaseCommand):
    help = 'initial upload of the mindmap content on the database and creation of the xml file containing correspondance'
    args = ""

    def add_arguments(self, parser):
        parser.add_argument(
            'filepath',
            nargs='?',
        )

    def handle(self, filepath, *args, **options):
        from django.conf import settings
        languages = [l['code'] for l in settings.CMS_LANGUAGES[1]]
        languages = options.get('languages', languages)
        lang = languages[0]
        session = default_session
        map = Map.load_from_file(filepath)
        subs = map.node.get_descendant('subscriptions')
        if subs:
            mm_subs = SubscriptionsNode(node=subs, language=lang, session=session)
            ps_repo = SubscriptionPlanSetRepository(session=session)
            p_repo = ps_repo.plan_repo
            for p in mm_subs.plans:
                p_repo.create_or_update_db(p)
            for ps in mm_subs.plansets:
                ps_repo.create_or_update_db(ps)
            assert mm_subs

