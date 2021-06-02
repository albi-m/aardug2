# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
from odoo import api, fields, models,_

class website_emails(models.Model):
    _name = "website.email"
    _description = 'pricelist pdf send on emails'

    name = fields.Char('Email')
    company_id = fields.Many2one('res.company', string='Company')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachment Files',
                                      help="You may attach files to this record.")

