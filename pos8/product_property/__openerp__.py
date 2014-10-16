# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-2013 Serpent Consulting Services Pvt. Ltd. (<http://serpentcs.com>).
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
    "name" : "Product Property",
    "version" : "1.0",
    "author": "Serpent Consulting Services",
    "website": "http://www.serpentcs.com",
    "category" : "Corporate ",
    "description": """Managing product Information for a company""",
    "depends" : ["product", "point_of_sale"],
    "update_xml" : ['product_property_view.xml',
                    'product_inherit.xml'],
    'data': [
        'security/ir.model.access.csv',
        ],
    'demo':['demo/product_property_demo.xml',],
    "installable": True,
    "auto_install": False,
    "application": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: