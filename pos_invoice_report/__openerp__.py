# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#    Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'POS Invoice QR Code Report',
    'version': '0.01',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Accounting',
    'description' : """
It prints the customer POS invoice reports with QR code.
    """,
    'website': 'http://www.serpentcs.com',
    'depends': ['point_of_sale_table', 'account_invoice_report', ],
    'data': [
         'security/ir.model.access.csv',
         'pos_invoice_view.xml',
         'view/templates.xml',
         'qr_sequence.xml',
         'pos_qr_report.xml',
         'wizard/pos_invoice_format_a_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
