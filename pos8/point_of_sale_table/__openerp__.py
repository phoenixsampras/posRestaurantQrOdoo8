# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-2014 Serpent Consulting Services Pvt. Ltd. (<http://serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Point of Sale Table',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'sequence': 6,
    'summary': 'Touchscreen Interface for Shops',
    'description': """
Quick and Easy sale process
===========================

This module allows you to manage your shop sales very easily with a fully web based touchscreen interface.
It is compatible with all PC tablets and the iPad, offering multiple payment methods. 

Product selection can be done in several ways: 

* Using a barcode reader
* Browsing through categories of products or via a text search.

Main Features
-------------
* Fast encoding of the sale
* Choose one payment method (the quick way) or split the payment between several payment methods
* Computation of the amount of money to return
* Create and confirm the picking list automatically
* Allows the user to create an invoice automatically
* Refund previous sales
    """,
    'author': 'Serpent Consulting Services Pvt. Ltd',
    'installable': True,
    'application': True,
    'demo':['demo/point_of_sale_table_data.xml',],
    'data':['security/pos_table_security.xml',
            'security/ir.model.access.csv',
            'point_of_sale_sequence.xml',
            'wizard/waiting_queue_allow_state_view.xml',
            'view/templates.xml',
            'point_of_sale_table_view.xml',
            ],
    'depends': ['point_of_sale','pos_restaurant','product_property'],
    'qweb': ['static/src/xml/pos.xml'],
    'auto_install': False,     
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
