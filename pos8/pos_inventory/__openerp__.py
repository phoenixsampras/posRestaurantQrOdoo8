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
    'name': 'Point of Sale Inventory',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'sequence': 6,
    'summary': "Manage Inventory In Point Of Sale.",
    'description': """This module is used for manage inventory in point of sale.
        When confirm the point of sale order then it will create the procurement order of each order line same as sale order.
    """,
    'author': 'Serpent Consulting Services',
    'images': [],
    'depends': ['mrp', 'purchase', 'point_of_sale_table'],
    'data': ['security/ir.model.access.csv', 'pos_inventory_view.xml'],
    'demo':[],
    'installable': True,
    'application': True,
    'js': [],
    'css': [],
    'qweb': [],
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
