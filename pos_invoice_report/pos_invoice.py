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

from openerp.osv import orm,fields
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from httplib2 import Http
from BeautifulSoup import BeautifulSoup
import subprocess
import urllib, urllib2
from urllib import urlencode
from openerp import workflow
from openerp.tools.translate import _

class pos_config(orm.Model):
    _inherit = 'pos.config'
    _columns = {
        'is_qr_report' : fields.boolean('Print Invoice with QR'),
    }

class pos_session(orm.Model):
    _inherit = 'pos.session'
    _columns ={
        'qr_code_ids': fields.many2many('qr.code', 'pos_invoice_rel_qr_code', 'session_id', 'qr_id', 'Dosificacion Tienda'),
    }

class pos_order(orm.Model):
    _inherit = 'pos.order'
    
    def _count_amt(self, cr, uid, ids, name, args, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context):
            result[data.id] = data.amount_total * 0.13 or 0.00
        return result

    def _count_control_code(self, cr, uid, ids, name, args, context=None):
        result = {}
        date = False
        for data in self.browse(cr, uid, ids, context):
            if data.date_order:
                date = datetime.datetime.strptime(data.date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime('%Y%m%d')
            h = Http()
            url_data = dict(AUTH_NUMBER=int(data.qr_code_id.auth_number),ORDER_NUMBER=int(data.qr_order_no),NIT_CODE_CUSTOMER=int(data.nit),DATE=int(date),AMOUNT=data.amount_total,KEYGEN=str(data.qr_code_id.keygen or ''))
            url= urlencode(url_data)
            resp = urllib2.urlopen('http://198.178.122.145:8060/cc/codigo_control.php?'+url)
            soup = BeautifulSoup(resp)
            result[data.id] = str(soup) or ''
        return result

    def _get_month_first_date(self, cr, uid, ids, name, args, context=None):
        result = {}
        for data in self.browse(cr, uid, ids):
            today_date = datetime.date.today().strftime('%d')
            if today_date == 1:
                seq = {
                    'name': 'QR POS Invoice',
                    'implementation':'standard',
                    'code': 'pos.order',
                    'prefix': '',
                    'padding': 1,
                    'number_increment': 1
                }
                self.pool.get('ir.sequence').create(cr, uid, seq)
            result[data.id] = today_date
        return result

    def _get_qr_code(self, cr, uid, ids, context=None):
        s = self.browse(cr, uid, ids)
        qr_code_ids = self.pool.get('pos.order').search(cr, uid, [('qr_code_id', 'in', ids)], context=context)
        return qr_code_ids

    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('pos.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns = {
        'qr_code_id': fields.many2one('qr.code', 'Dosificacion Tienda'),
        'nit': fields.char('NIT', size=11),
        'legal_customer_name': fields.char('Legal Name Customer', size=32),
        'razon': fields.char('Razón Social',size=124,help="Nombre o Razón Social para la Factura."),
        'amt_thirteen': fields.function(_count_amt, string="Amount*0.13", type='float'),
        'qr_order_no': fields.char('QR Invoice Number', size=32),
        'get_month_first_date': fields.function(_get_month_first_date, string="Month Date", type="integer"),
        'control_code': fields.function(_count_control_code, string="Control Code", type='char', size=17, store=
                    {
                    'pos.order': (lambda self, cr, uid, ids, c={}: ids, ['qr_code_id', 'nit', 'date_order', 'qr_order_no', 'amount_total'], 10),
                    'pos.order.line': (_get_invoice_line, ['price_unit','qty','discount','order_id'], 20),
                    'qr.code': (_get_qr_code, ['auth_number', 'keygen', 'nit_code_comapny'], 10),
                }),
    }

    _defaults = {
        'qr_order_no': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'pos.qr.code.order'),
    }

    def onchange_session_id(self, cr, uid, ids, session_id, context=None):
        domain = {}
        data = self.pool.get('pos.session').browse(cr, uid, session_id, context=context)
        qr_code_ids = [qr.id for qr in data.qr_code_ids]
        
        domain = [('id', '=', qr_code_ids)]
        return {'domain': {'qr_code_id': domain}}

    def onchange_partner_id(self, cr, uid, ids, part=False, context=None):
        result = super(pos_order,self).onchange_partner_id(cr, uid, ids, part, context)
        if part:
            p = self.pool.get('res.partner').browse(cr, uid, part, context=context)
            result['value']['nit'] = p.commercial_partner_id.nit
            result['value']['legal_customer_name'] = p.legal_name_customer
        return result

    def create_from_ui(self, cr, uid, orders, kitchen=False,confirm = False, context=None):
        order_ids = []
        pos_line_object = self.pool.get('pos.order.line')
        table_reserved_obj = self.pool.get("table.reserverd")
        session_obj = self.pool.get('pos.session')
        shop_obj = self.pool.get('sale.shop')
        for tmp_order in orders:
            to_invoice = tmp_order.get('to_invoice')
            if tmp_order.get('data'):
                order = tmp_order['data']
            else:
                order = tmp_order
            user_id = order.get('user_id')
        sql = """
            SELECT id
            FROM pos_session
            WHERE user_id = %d and state = 'opened';

        """ % (int(user_id))
        cr.execute(sql)
        tmp_data = cr.fetchall()
        if not tmp_data:
            raise orm.except_orm(_('error!'), _('"No Point Of Sale Found For User.'))
        else:
            if tmp_data:
                order.update({"pos_session_id":tmp_data[0][0]})
            if order.get('id'):
                created_order = self.browse(cr, uid, order.get('id'), context=context)
                if order.get('user_id') and created_order.user_id.id != order.get('user_id'):
                    self.write(cr, uid, created_order.id, {'user_id':order.get('user_id')}, context=context)
                line_ids = [line.id for line in created_order.lines]
                table_data = order.get("table_data")
                reserve_table_ids = []
                if table_data:
                    self.write(cr, uid, order.get('id'), {'reserved_table_ids': [(5,0)]}, context = context)
                    for reserve in table_data:
                        reserve.update({"order_id":order.get('id')})
                        reserv_id = self.pool.get("table.reserverd").create(cr, uid, reserve, context = context)
                        reserve_table_ids.append((4,reserv_id))
                        self.write(cr, uid, [order.get('id')], {'reserved_table_ids': reserve_table_ids}, context = context)
                if tmp_order.get('partner_id'):
                    self.write(cr, uid, [order.get('id')], {'partner_id': tmp_order.get('partner_id')}, context = context)
                if line_ids:
                    for line in order.get('lines'):
                        if line[2] and line[2].get('id') and line[2].get('id') in line_ids:
                            pos_line_object.write(cr, uid, [int(line[2].get('id'))], {'property_description':line[2].get('property_description') or '',
                                                         'discount':line[2].get('discount'),
                                                         'price_unit':line[2].get('price_unit'),
                                                        'product_id':line[2].get('product_id'),
                                                        'product_ids': line[2].get('product_ids'),
                                                        'qty':line[2].get('qty'),
                                                        'order_line_state_id': line[2].get('wait_text') and 5 or 1,
                                                        'flag':True}, context = context)
                for line in order.get('lines'):
                    if line[2] and not line[2].get('id'):
                        pos_line_object.create(cr, uid, {'property_description':line[2].get('property_description') or '',
                                                             'discount':line[2].get('discount'),
                                                             'price_unit':line[2].get('price_unit'),
                                                            'product_id':line[2].get('product_id'),
                                                            'product_ids': line[2].get('product_ids'),
                                                            'qty':line[2].get('qty'),
                                                            'order_id':order.get('id'),
                                                            'flag':True,
                                                            'order_line_state_id': line[2].get('wait_text') and 5 or 1,
                                                            }, context = context)
                if kitchen:
                    created_order = self.browse(cr, uid, order.get('id'), context=context)
                    line_ids = [line.id for line in created_order.lines]
                    return [order.get('id'), line_ids]
                else: 
                    order_id = order.get('id')
            else:
                table_data = order.get("table_data")
                tables = []
                partner_nit = ''
                if order.get('partner_id',False):
                    partner_id = order.get('partner_id',False)
                    partner_nit = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context).nit
                if table_data:
                    for reserve in table_data:
                        table_id = reserve.get('table_id')
                        reserv_id = self.pool.get("table.reserverd").create(cr, uid, reserve, context = context)
                        tables.append((4,reserv_id))
                    for line in order.get('lines'):
                        line[2].update({'flag':True,'order_line_state_id':line[2].get('wait_text') and 5 or 1})
                    order_id = self.create(cr, uid, {
                        'name': order['name'],
                        'qr_code_id': order['qr_code_id'] or False ,
                        'phone': order['phone'] or False,
                        'split_order': order['split_order'] or False,
                        'user_id': order['user_id'] or False,
                        'partner_id': order.get('partner_id'),
                        'nit': partner_nit or False,
                        'pricelist_id': order.get('pricelist_id'),
                        'session_id': order['pos_session_id'],
                        'lines': order['lines'],
                        'pos_reference':order['name'],
                        'reserved_table_ids': tables,
                    }, context)

                if not table_data:
                    for line in order.get('lines'):
                        line[2].update({'flag':True,'order_line_state_id':line[2].get('wait_text') and 5 or 1})
                    order_id = self.create(cr, uid, {
                        'name': order['name'],
                        'qr_code_id': order['qr_code_id'] or False ,
                        'user_id': order['user_id'] or False,
                        'driver_name': order.get('driver_name',False),
                        'phone': order.get('phone',False),
                        'split_order': order['split_order'] or False,
                        'partner_id': order.get('partner_id'),
                        'nit': partner_nit or False,
                        'pricelist_id': order.get('pricelist_id'),
                        'session_id': order['pos_session_id'],
                        'lines': order['lines'],
                        'pos_reference':order['name'],
                        'pflag': order.get('pflag', False),
                        'parcel':order.get('parcel', False),
                    }, context)

                created_order = self.browse(cr, uid, order_id, context=context)
                line_ids = [line.id for line in created_order.lines]
                if kitchen:
                    return [order_id, line_ids]
            if not kitchen and not confirm:
                for payments in order['statement_ids']:
                    payment = payments[2]
                    self.add_payment(cr, uid, order_id, {
                        'amount': payment['amount'] or 0.0,
                        'payment_date': payment['name'],
                        'statement_id': payment['statement_id'],
                        'payment_name': payment.get('note', False),
                        'journal': payment['journal_id']
                    }, context=context)

                if order['amount_return']:
                    session = self.pool.get('pos.session').browse(cr, uid, order['pos_session_id'], context=context)
                    cash_journal = session.cash_journal_id
                    if not cash_journal:
                        cash_journal_ids = filter(lambda st: st.journal_id.type == 'cash', session.statement_ids)
                        if not len(cash_journal_ids):
                            raise orm.except_orm(_('error!'),
                                _("No cash statement found for this session. Unable to record returned cash."))
                        cash_journal = cash_journal_ids[0].journal_id
                    self.add_payment(cr, uid, order_id, {
                        'amount':-order['amount_return'],
                        'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'payment_name': _('return'),
                        'journal': cash_journal.id,
                    }, context=context)
                order_ids.append(order_id)
                workflow.trg_validate(uid, 'pos.order', order_id, 'paid', cr)
            else:
                order_ids.append(order_id)

            if to_invoice:
                self.action_invoice(cr, uid, [order_id], context)
                order_obj = self.browse(cr, uid, order_id, context)
                self.pool['account.invoice'].signal_workflow(cr, uid, [order_obj.invoice_id.id], 'invoice_open')
            return order_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: