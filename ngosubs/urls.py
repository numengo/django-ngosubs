# -*- coding: utf-8 -*-
"""paths for the Flexible Subscriptions app."""
# pylint: disable=line-too-long
import importlib
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from .conf import SETTINGS


app_name = 'ngosubs'

# Retrieve the proper subscribe view
SubscribeView = getattr(  # pylint: disable=invalid-name
    importlib.import_module(SETTINGS['subscribe_view']['module']),
    SETTINGS['subscribe_view']['class']
)


urlpatterns = [
    url(
        r'subscribe/',
        views.SubscribeList.as_view(),
        name='dfs_subscribe_list',
    ),
    url(
        r'subscribe/add/',
        SubscribeView.as_view(),
        name='dfs_subscribe_add',
    ),
    url(
        r'subscribe/thank-you/<uuid:transaction_id>/',
        views.SubscribeThankYouView.as_view(),
        name='dfs_subscribe_thank_you',
    ),
    url(
        r'subscribe/cancel/<uuid:subscription_id>/',
        views.SubscribeCancelView.as_view(),
        name='dfs_subscribe_cancel',
    ),
    url(
        r'subscriptions/',
        views.SubscribeUserList.as_view(),
        name='dfs_subscribe_user_list',
    ),
    url(
        r'dfs/tags/',
        views.TagListView.as_view(),
        name='dfs_tag_list',
    ),
    url(
        r'dfs/tags/create/',
        views.TagCreateView.as_view(),
        name='dfs_tag_create',
    ),
    url(
        r'dfs/tags/<int:tag_id>/',
        views.TagUpdateView.as_view(),
        name='dfs_tag_update',
    ),
    url(
        r'dfs/tags/<int:tag_id>/delete/',
        views.TagDeleteView.as_view(),
        name='dfs_tag_delete',
    ),
    url(
        r'dfs/plans/',
        views.PlanListView.as_view(),
        name='dfs_plan_list',
    ),
    url(
        r'dfs/plans/create/',
        views.PlanCreateView.as_view(),
        name='dfs_plan_create',
    ),
    url(
        r'dfs/plans/<uuid:plan_id>/',
        views.PlanUpdateView.as_view(),
        name='dfs_plan_update',
    ),
    url(
        r'dfs/plans/<uuid:plan_id>/delete/',
        views.PlanDeleteView.as_view(),
        name='dfs_plan_delete',
    ),
    url(
        r'dfs/plan-lists/',
        views.PlanListListView.as_view(),
        name='dfs_plan_list_list',
    ),
    url(
        r'dfs/plan-lists/create/',
        views.PlanListCreateView.as_view(),
        name='dfs_plan_list_create',
    ),
    url(
        r'dfs/plan-lists/<int:plan_list_id>/',
        views.PlanListUpdateView.as_view(),
        name='dfs_plan_list_update',
    ),
    url(
        r'dfs/plan-lists/<int:plan_list_id>/delete/',
        views.PlanListDeleteView.as_view(),
        name='dfs_plan_list_delete',
    ),
    url(
        r'dfs/plan-lists/<int:plan_list_id>/details/',
        views.PlanListDetailListView.as_view(),
        name='dfs_plan_list_detail_list',
    ),
    url(
        r'dfs/plan-lists/<int:plan_list_id>/details/create/',
        views.PlanListDetailCreateView.as_view(),
        name='dfs_plan_list_detail_create',
    ),
    url(
        r'dfs/plan-lists/<int:plan_list_id>/details/<int:plan_list_detail_id>/',
        views.PlanListDetailUpdateView.as_view(),
        name='dfs_plan_list_detail_update',
    ),
    url(
        r'dfs/plan-lists/<int:plan_list_id>/details/<int:plan_list_detail_id>/delete/',
        views.PlanListDetailDeleteView.as_view(),
        name='dfs_plan_list_detail_delete',
    ),
    url(
        r'dfs/subscriptions/',
        views.SubscriptionListView.as_view(),
        name='dfs_subscription_list',
    ),
    url(
        r'dfs/subscriptions/create/',
        views.SubscriptionCreateView.as_view(),
        name='dfs_subscription_create',
    ),
    url(
        r'dfs/subscriptions/<uuid:subscription_id>/',
        views.SubscriptionUpdateView.as_view(),
        name='dfs_subscription_update',
    ),
    url(
        r'dfs/subscriptions/<uuid:subscription_id>/delete/',
        views.SubscriptionDeleteView.as_view(),
        name='dfs_subscription_delete',
    ),
    url(
        r'dfs/transactions/',
        views.TransactionListView.as_view(),
        name='dfs_transaction_list',
    ),
    url(
        r'dfs/transactions/<uuid:transaction_id>/',
        views.TransactionDetailView.as_view(),
        name='dfs_transaction_detail',
    ),
    url(
        r'dfs/',
        views.DashboardView.as_view(),
        name='dfs_dashboard',
    ),
]
