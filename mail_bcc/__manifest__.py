# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Email Bcc',
    'version': '14.0.1.0',
    'license': 'OPL-1',
    'category': 'Tools',
    'summary': 'This plug-in allows way for a Bcc address in Email & Templates.',
    'description': """
Add support of Bcc address in email template and send those email to Bcc
address in email. The Bcc email address is not supported by odoo standard.
    """,
    'company': 'Caret IT Solutions Pvt. Ltd.',
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'maintainer': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'https://www.caretit.com',
    'depends': ['mail'],
    'data': [
        'views/mail_template_view.xml',
        'views/mail_mail_view.xml',
    ],
    'images': ['static/description/banner.gif'],
    'price': 15.00,
    'currency': 'EUR',
}
