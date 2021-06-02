# -*- coding: utf-8 -*-

from odoo import fields, http
from odoo.http import request

class WebsiteEmailMail(http.Controller):

    @http.route(['/website_form/email/submit'],
        type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def website_email_mail(self, name, **kw):
        """ Send pricelist pdf to contact person by mail"""

        MassMailContact = request.env['website.email']
        website_email_id = MassMailContact.create({
                            'name': name, 
                            'company_id': request.website.company_id.id,
                        })
        template_id = request.env.ref('website_email_snippet.email_template_website_email',
            raise_if_not_found=False).sudo()
        if template_id:
            if template_id.attachment_ids:
                website_email_id.attachment_ids = template_id.attachment_ids.ids
            template_id.send_mail(website_email_id.id, force_send=True)
        return request.redirect('/prijslijst-bedankt')


    @http.route(['/render/template'], type='json', auth="public", website=True)
    def get_template(self, **kw):
        partner_bottom_template = request.env.ref('website_email_snippet.odoo_partner')
        partner_bottom_temp_add = partner_bottom_template.arch_base
        return {'partner_bottom_template': partner_bottom_temp_add}
