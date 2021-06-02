# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import re

from odoo import api, models, _
from odoo import tools

def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        return s[start:s.rindex(last, start)]
    except ValueError:
        return ""


class crm_lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def bezoekverslag_parser(self, emailBody):
        """This Method returns plain text dict for
        Template Offerte aanvraag
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        a = find_between_r(plain_text_body, 'Trigger Bezoeker', '').split('\n')
        
        if len(a) > 1:
            addresindex = [i for i, s in enumerate(a) if 'Straat' in s]
            if addresindex and addresindex[0]:
                newdict['Adres:'] = str(a[addresindex[0]+1])
            postcodeindex = [i for i, s in enumerate(a) if 'Postcode' in s]
            if postcodeindex and postcodeindex[0]:
                newdict['Postcode:'] = a[postcodeindex[0]+1]
            cityindex = [i for i, s in enumerate(a) if 'Plaats' in s]
            if cityindex and cityindex[0]:
                newdict['Plaats:'] = a[cityindex[0]+1]
            telephoneindex = [i for i, s in enumerate(a) if 'Telefoonnummer' in s]
            if telephoneindex and telephoneindex[0]:
                newdict['Telefoon:'] = a[telephoneindex[0]+1]

            description = ''           
            data = [i for i, s in enumerate(a) if '0u 9m 56s' in s]
            if data and data[0]:
                description += '\n'+'0u 9m 56s:'+' '+a[data[0]+1].replace('*', '')            
            data = [i for i, s in enumerate(a) if '0u 0m 5s' in s]
            if data and data[0]:
                description += '\n'+'0u 0m 5s:'+' '+a[data[0]+1].replace('*', '')
            data = [i for i, s in enumerate(a) if '0u 0m 41s' in s]
            if data and data[0]:
                description += '\n'+'0u 0m 41s:'+' '+a[data[0]+1].replace('*', '')
            newdict['Toelichting:'] = description
        return newdict

    @api.model
    def bezoekverslag_condition(self, mailMessage, emailBody):
        """Condition for Offerte aanvraag template."""
        return (mailMessage.xaa_aa_company == 'bezoekverslag' or
                'Website' in emailBody)

    @api.model
    def register_company_parser(self):
        """Register Offerte aanvraag Parser Mappin in main."""
        parsers = super(crm_lead, self).register_company_parser()
        parsers.append(
            (10,
             self.bezoekverslag_condition,
             self.bezoekverslag_parser))
        return parsers
