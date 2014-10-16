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

from openerp.osv import osv, fields

class ProductProperty(osv.osv):
    _name = 'product.property'
    
    _columns = {
              'name':fields.char('Product Property' , size=64, required=True, help='Enter Product Name'),
              'product_attribute_ids':fields.many2many('product.product', 'rel_product_property_atrributes','product_property_id', 'product_product_id', 'Attribute'),
              'product_ids':fields.many2many('product.product', 'rel_product_property', 'product_property_id', 'product_product_id', 'Product'),
              'single_choice': fields.boolean('Single Choice'),
    }
ProductProperty()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
class ProductInherits(osv.osv):
    _inherit = 'product.product'
    
    _columns = {
              'is_customizable':fields.boolean("Is Customizable?"),
              'property_ids':fields.many2many('product.property', 'rel_product_property', 'product_product_id', 'product_property_id', 'Product')
    }
ProductInherits()

