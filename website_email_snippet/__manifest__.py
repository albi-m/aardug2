# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name' : 'Website email snippet',
    'version': '14.0.1.0',
    'summary': '',
    'category': 'website',
    'description': """ This module aim is get emails from website and then send mail on that emails.
                    1. Add snippet on website for get emails from customer.
                    2. After submit email, system will check email is valide or not.
                    3. Show all customer emails in website menu (Website Email).
                    4. After submit email, system will send mail on that email with attachment file.
                    5. Add mail template 'Pricelist PDF - Send by Email' for send mail""",
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'depends': ['website'],
    'data': [
             'security/ir.model.access.csv',
             'data/data.xml',
             'views/assets.xml',
             'views/website_email_view.xml',
             'views/snippet.xml',
            ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
