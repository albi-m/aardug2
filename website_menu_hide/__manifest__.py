# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name' : 'Website hide menu',
    'version': '14.0.1.0',
    'summary': '',
    'category': 'website',
    'description': """Hide some menus on website for portal user""",
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'depends': ['website'],
    'data': [
            'views/website_menu_view.xml',
            'views/website_template.xml',
            ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
