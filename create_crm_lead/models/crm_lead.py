# -*- encoding: utf-8 -*-


import logging
import re
from odoo import api, fields, models, _
from odoo import tools


_logger = logging.getLogger(__name__)


def clear_string(strng, strip=False):
    # Replace new line from string
    if strip:
        return strng.strip()
    return strng.replace('\n', '').replace('\r', '').strip()


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    xaa_aa_email_description = fields.Html(
        'Email Description', translate=True,
        help='store html body of email lead which is create from fetch mail')

    @api.model_create_multi
    def create(self, vals_list):
        # Remove unnecessory character from email_from
        for vals in vals_list:
            if vals.get('email_from'):
                if '<' and '>' in vals.get('email_from'):
                    pemail = vals.get('email_from').split('<')
                    vals['email_from'] = pemail[1].replace(
                        "u'", " ").replace(">'", "").replace('>', '')
        return super(CrmLead, self).create(vals_list)

    @api.model
    def register_company_parser(self):
        """Return company mapping(list of tuple) for extension of new templates
        for lead information parsing from incoming email body.

        i.e: (priority, condition, parser) where #1 is condition for company
        and #2 is for collecting information from email body parser.

        priority: This parser executed in order by priority.

        condition: This can be a function which can accept two arguments as
        following.
        mailMessage = respected mail.message record.
        emailBody = html email body which received and parsing in progress for
        crm lead record.

        parser: This must be your parser and should return dictionary with
        respected valid values to be filled on lead record. Check code of
        create_crm_lead module for more detail. If key(condition) returns
        True value(parser) will be called with email body in argument.

        You can override this function and add your template setup.
        """
        return []

    @api.model
    def _build_valid_dict(self, newdict):
        """
            preparing valid dictionary which has key as crm.lead fields
        """
        validDict = {}
        contactNames = []
        if newdict.get('Voornaam:', '') or newdict.get('Voornaam', ''):
            contactNames.append(
                clear_string(newdict.get('Voornaam:', '') or
                             newdict.get('Voornaam', ''),
                             True))
        if newdict.get('Naam:', '') or newdict.get('Naam', ''):
            contactNames.append(
                clear_string(newdict.get('Naam:', '') or
                             newdict.get('Naam', ''),
                             True))
        if newdict.get('name:'):
            validDict['name'] = clear_string(newdict.get('name:', ''),True)
        if newdict.get('partner_name:'):
            validDict['partner_name'] = clear_string(newdict.get('partner_name:', ''),True)
        if newdict.get('Achternaam:', '') or newdict.get('Achternaam', ''):
            contactNames.append(
                clear_string(newdict.get('Achternaam:', '') or
                             newdict.get('Achternaam', ''),
                             True))
        if newdict.get('Contact:', ''):
            contactNames.append(
                clear_string(newdict.get('Contact:', ''), True))
        if contactNames:
            validDict['contact_name'] = ' '.join(contactNames)
        if newdict.get('E-mail:', ''):
            email = clear_string(newdict.get('E-mail:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            validDict['email_from'] = email
        if newdict.get('E-mailadres:', ''):
            email = clear_string(newdict.get('E-mailadres:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            validDict['email_from'] = email
        if newdict.get('E-mail adres:', ''):
            email = clear_string(newdict.get('E-mail adres:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            validDict['email_from'] = email
        if newdict.get('Email adres:', ''):
            email = clear_string(newdict.get('Email adres:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            validDict['email_from'] = email
        if (newdict.get('Telefoon:', '') or
                newdict.get('Telefoonnummer:', '') or
                newdict.get('Telefoonnummer 1', '') or
                newdict.get('Tel.:', '')):
            validDict['phone'] = clear_string(
                newdict.get('Telefoon:', '') or
                newdict.get('Telefoonnummer:', '') or
                newdict.get('Telefoonnummer 1', '') or
                newdict.get('Tel.:', ''),
                True)
        if newdict.get('Mobiel:', ''):
            validDict['mobile'] = clear_string(
                newdict.get('Mobiel:', ''), True)
        if newdict.get('Adres:', '') or newdict.get('Straat:', ''):
            validDict['street'] = clear_string(
                newdict.get('Adres:', '') or newdict.get('Straat:', ''), True)
        if newdict.get('Straatnaam:', ''):
            if 'google' in newdict.get('Straatnaam:', '').lower():
                street = newdict.get('Straatnaam:', '')
                street = re.sub(r'\([^)]*\)', '', street)
            else:
                street = newdict.get('Straatnaam:', '')
            validDict['street'] = clear_string(street, True)
        if newdict.get('Postcode:', ''):
            validDict['zip'] = clear_string(
                newdict.get('Postcode:', ''), True)
        if newdict.get('Postal:', ''):
            validDict['zip'] = clear_string(newdict.get('Postal:', ''), True)
        if (newdict.get('Woonplaats:', '') or
                newdict.get('Plaats:', '') or
                newdict.get('Stad:', '') or
                newdict.get('Plaatsnaam:', '')):
            validDict['city'] = clear_string(
                newdict.get('Woonplaats:', '') or
                newdict.get('Plaats:', '') or
                newdict.get('Stad:', '') or
                newdict.get('Plaatsnaam:', ''),
                True)
        if newdict.get('Toelichting:', ''):
            validDict['description'] = clear_string(
                newdict.get('Toelichting:', ''), True)
        if newdict.get('Website:', ''):
            validDict['website'] = clear_string(
                newdict.get('Website:', ''), True)
        if newdict.get('Functie:', ''):
            validDict['function'] = clear_string(
                newdict.get('Functie:', ''), True)
        if newdict.get('Regio:'):
            validDict['state_id'] = newdict.get('Regio:')
        return validDict

    def update_res_partner(self, partner, netherlands):
        """
            if new lead has partner than update partner
        """
        binnenland = self.env['account.fiscal.position'].search(
            [('name', '=', 'Binnenland')])
        days15 = self.env['account.payment.term'].search(
            [('name', '=', '15 Days')])
        partner.write({
            'country_id': netherlands and netherlands.id or False,
            'property_account_position_id': binnenland and binnenland.id or False,
            'lang': 'nl_NL',
            'property_payment_term_id': days15 and days15.id or False
        })

    @api.model
    def create_lead_from_email_body(self):
        mailMsgObj = self.env['mail.message']
        leadId = self.browse(self.env.context.get('active_id'))
        if leadId.email_from:
            companyname = ''
            emailfromat = leadId.email_from.split('@')
            if len(emailfromat) == 2:
                # Get company name from email id
                emailfromdot = emailfromat[1].split('.')
                companyname = emailfromdot[0]
            subtypeId = self.env.ref('crm.mt_lead_create')
            messageIds = mailMsgObj.search([
                ('res_id', '=', leadId.id),
                ('model', '=', 'crm.lead'),
                ('message_type', '=', 'email'),
                ('subtype_id', '=', subtypeId.id)])
            messageIds.write({'xaa_aa_company': companyname})
            _logger.info(
                '%s create crm lead from mail %s \n'
                'Crm Lead Record ID ::::: (%s) \n'
                'Crm Lead Subject Name ::::: %s' % (
                    len(messageIds),
                    leadId.id,
                    leadId.id,
                    leadId.name or '')
                )
            if not messageIds:
                return True
            # if get more than 1 message then only take one of them
            htmlBody = messageIds[0].read(['body'])[0].get('body')
            newdict = {}
            try:
                conditionalParsers = sorted(self.register_company_parser(),
                                            key=lambda x: x[0])
                for priority, condition, parser in conditionalParsers:
                    if condition(mailMessage=messageIds[0], emailBody=htmlBody):
                        # Calling parser to parse html body and return dict
                        # which has key as valid name to be map for lead model
                        newdict.update(parser(emailBody=htmlBody))
                if newdict:
                    validDict = self._build_valid_dict(newdict)
                    if validDict:
                        validDict['xaa_aa_email_description'] = htmlBody or ''
                        # Company name extract from lead email_from configured
                        # in mail lead source , searching for that here
                        netherlands = self.env['res.country'].search(
                            [('name', '=', 'Netherlands')])

                        partner = leadId.partner_id if leadId.partner_id else False
                        if partner:
                            self.update_res_partner(partner, netherlands) 
                        elif not partner:
                            validDict['country_id'] = netherlands and netherlands.id or False
                        emailTo = validDict.get('email_from')
                        if not emailTo:
                            emailTo = self.email_from or ''
                    # Assigning type lead
                    validDict['type'] = 'lead'
                    # Process all the pending computations
                    leadId.flush()
                    leadId.write(validDict)
            except Exception as e:
                _logger.info('Exception %s found' % e)
                _logger.info('parsing email template failed for %s lead id' % leadId.id)
                # Silently pass,
                # Email format is not known hence it will perform lead creation in
                # Odoo's default way, that is, using the header information.
                pass

        return True
