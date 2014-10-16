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

from openerp.osv import fields, orm

class pos_invoice_format_a(orm.TransientModel):
    
    _name = 'pos.invoice.format.a'
    _description = 'Pos Invoice Format A'

    _columns = {
            'period_id': fields.many2one('account.period', 'Period', required=True)
    }

    def print_invoice_format_a(self, cr, uid, ids, context):
        datas = {
            'ids': ids,
            'model': 'pos.order',
            'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pos_invoice_format_a',
            'datas': datas,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: