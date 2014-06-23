# coding=utf-8
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'iamcast.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name
from django.conf import settings

from datetime import datetime, date, timedelta


class CustomIndexDashboard(Dashboard):

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Viajante'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    column=1,
                    collapsible=False,
                    models=(
                      'viajante.models.Ciudad',
                      'viajante.models.Problema',
                      ),
                ),
            ]
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Administracion de usuarios y permisos'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=True,
            column=2,
        ))

