# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
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

from openerp.report import report_sxw
import datetime
import qrcode
import base64
import amount_to_text_es
import tempfile
from BeautifulSoup import BeautifulSoup
import subprocess
import urllib, urllib2
from urllib import urlencode
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class invoice_anverso(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(invoice_anverso, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_amount': self.get_amount,
            'get_qrcode': self.get_qrcode,
            'get_qrdate': self.get_qrdate,
            'get_datelimit': self.get_datelimit,
            'get_username': self.get_username,
        })

    def get_username(self):
        user_name = self.pool.get('res.users').browse(self.cr, self.uid, self.uid).name
        return user_name

    def get_datelimit(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

    def get_qrdate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

    def get_amount(self, amount, currency):
        amt_en = amount_to_text_es.amount_to_text(amount, 'en', currency)
        return amt_en

    def get_qrcode(self, auth_no, in_no, ncc, date, amt, keygen):
#        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
#        url = 'http://198.178.122.145:8060/cc/codigo_control.php?AUTH_NUMBER=' + str(auth_no or '') + '&ORDER_NUMBER=' + str(in_no or '') + '&NIT_CODE_CUSTOMER=' + str(ncc or '') + '&DATE=' + str(date or '') + '&AMOUNT=' + str(amt or '') + '&KEYGEN=' + str(keygen or '')
        date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT).strftime('%Y%m%d')
        control_code = str(auth_no or '') + '|' + str(in_no or '') + '|' + str(ncc or '') + '|' + str(date or '') + '|' + str(amt or '') + '|' + str(keygen or '')
#        resp = urllib2.urlopen(url)
#        soup = BeautifulSoup(resp)
        qr_img = qrcode.make(control_code)
        filename = str(tempfile.gettempdir()) + '/qrtest.png'
        qr_img.save(filename)
        return base64.encodestring(file(filename, 'rb').read())

report_sxw.report_sxw('report.pos_anverso_receipt', 'pos.order', 'addons/pos_invoice_report/report/invoice_anverso.rml', parser=invoice_anverso)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
