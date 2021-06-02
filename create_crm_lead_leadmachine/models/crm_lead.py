# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################


from odoo import api, tools, models


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        return s[start:s.rindex(last, start)]
    except ValueError:
        return ''


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def leadmachine_parser(self, emailBody):
        """This Method returns plain text dict for 
        Template duurzaamfunderingsherstel
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        # lead details
        result = find_between_r(plain_text_body, 'Gegevens aanvrager', 'Met vriendelijke groet').split('\n')
        if len(result) > 1:
            for value in result:
                if value.find('[') and value.find(']'):
                    for i in range(value.count(']')):
                        value = value.replace(value[value.find('['):value.find(']')+1],'')
                if 'Bedrijfsnaam' in value:
                    naam = value.split('Bedrijfsnaam ')[1]
                    newdict['name:'] = naam
                    newdict['partner_name:'] = naam
                elif 'Adres' in value:
                    naam = value.split('Adres ')[1]
                    newdict['Straatnaam:'] = naam
                elif 'E-mailadres' in value:
                    naam = value.split('E-mailadres ')[1]
                    newdict['E-mail:'] = naam
                elif 'Telefoonnummer' in value:
                    naam = value.split('Telefoonnummer ')[1]
                    newdict['Telefoon:'] = naam
                elif 'Plaats' in value:
                    naam = value.split('Plaats ')[1]
                    newdict['Plaats:'] = naam
                elif 'Postcode' in value:
                    naam = value.split('Postcode ')[1]
                    newdict['Postcode:'] = naam
                elif 'Voornaam' in value:
                    naam = value.split('Voornaam ')[1]
                    newdict['Voornaam:'] = naam
                elif 'Achternaam' in value:
                    naam = value.split('Achternaam ')[1]
                    newdict['Achternaam:'] = naam
                elif 'Website' in value:
                    naam = value.split('Website ')[1]
                    newdict['Website:'] = naam
                elif 'Functie' in value:
                    naam = value.split('Functie ')[1]
                    newdict['Functie:'] = naam
                elif 'Regio:' in value:
                    name = value.split('Regio: ')[1]
                    state_id = self.env['res.country.state'].sudo().search([('name', 'ilike', name)], limit=1)
                    newdict['Regio:'] = state_id and state_id.id or False
                    newdict['Toelichting:'] = result[result.index(value)+2]
        return newdict

    @api.model
    def leadmachine_condition(self, mailMessage, emailBody):
        """Condition for duurzaamfunderingsherstel template."""
        return (mailMessage.xaa_aa_company in ['totalwall', 'Totalwall', 'duurzaamfunderingsherstel'] or
                'LEADMACHINE' in emailBody)

    @api.model
    def register_company_parser(self):
        """Register duurzaamfunderingsherstel Parser Mappin in main."""
        parsers = super(CrmLead, self).register_company_parser()
        parsers.append(
            (3,
             self.leadmachine_condition,
             self.leadmachine_parser)
        )
        return parsers
