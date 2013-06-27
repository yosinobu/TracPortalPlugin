# -*- coding: utf-8 -*-
#
# The user interface module for timeline of available projects.
#
# (C) 2013 Internet Initiative Japan Inc.
# All rights reserved.
#
# Created on 2013/05/20
# @author: yosinobu

__author__ = 'yosinobu'

from  pkg_resources import resource_filename

from genshi.builder import tag

from trac.core import *
from trac.web.chrome import INavigationContributor, ITemplateProvider, \
    add_script, add_stylesheet, add_script_data
from trac.web.api import IRequestHandler
from trac.perm import IPermissionRequestor

from tracportal.api import IProjectListProvider
from tracportal.i18n import _
from tracportal.project_list.api import IProjectInfoProvider


class DashboardModule(Component):
    implements(INavigationContributor, IPermissionRequestor, IRequestHandler, ITemplateProvider)

    project_list_providers = ExtensionPoint(IProjectListProvider)
    project_info_providers = ExtensionPoint(IProjectInfoProvider)

    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return 'dashboard'

    def get_navigation_items(self, req):
        if 'PORTAL_DASHBOARD_VIEW' in req.perm:
            yield ('mainnav', 'dashboard',
                   tag.a(_('Dashboard'), href=req.href('/dashboard'), accesskey=6))

    # IPermissionRequestor methods
    def get_permission_actions(self):
        return ['PORTAL_DASHBOARD_VIEW']

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info and req.path_info.startswith('/dashboard')

    def process_request(self, req):
        req.perm.require('PORTAL_DASHBOARD_VIEW')
        data = {}
        # Add scripts/styles
        add_stylesheet(req, 'tracportal/css/dashboard.css')
        add_stylesheet(req, 'tracportal/css/smoothness/jquery-ui-1.10.3.custom.min.css')
        add_stylesheet(req, 'common/css/report.css')
        if req.locale is not None:
            add_script(req, 'tracportal/js/messages/%s.js' % req.locale)
        add_script(req, 'tracportal/js/dashboard.js')
        add_script(req, 'tracportal/js/jquery-1.9.1.js')
        add_script(req, 'tracportal/js/jquery-ui-1.10.3.custom.min.js')
        # data['_'] = _
        add_script_data(req, {
            'tracportal': {
                'authname': req.authname
            }
        })
        return "dashboard.html", data, None

    # ITemplateProvider methods
    def get_htdocs_dirs(self):
        return [('tracportal', resource_filename('tracportal', 'htdocs'))]

    def get_templates_dirs(self):
        return [resource_filename('tracportal.dashboard', 'templates')]