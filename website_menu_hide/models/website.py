# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
from odoo import api, fields, models,_
from odoo.http import request

class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    hide_for_portal = fields.Boolean('Hide for portal')


    def check_menu_access(self):
        login_user = request.env.user
        if login_user.has_group('base.group_portal') and self.hide_for_portal:
            return False
        return True
