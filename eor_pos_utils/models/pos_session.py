# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import json
_logger = logging.getLogger(__name__)

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _compute_payments(self):
        list_payment = []
        for session in self:
            AccountPaymentObj = self.env['account.payment']
            journals = self.env['account.journal'].sudo().search([])
            domain = [('journal_id', 'in', journals.ids), ('es_abono', '=', True), ('abono_para', '=', 'debit')]
            payments = AccountPaymentObj.sudo().search(domain)
            session.payment_lines = payments
            pays = AccountPaymentObj.sudo().read_group(domain, ['journal_id', 'partner_id', 'amount'], ['journal_id'])
            partner_id = payments.mapped('partner_id')
            amount = payments.mapped('amount')
            journal_id = payments.mapped('journal_id')
            msg = ''
            for p in pays:
                msg += "%s %s \n" % (p['journal_id'][1], p['amount'])
            
            session.abono_total_debito = msg

    payment_lines = fields.One2many('account.payment', 'pos_session_id', string='Pagos', compute='_compute_payments')
    abono_total_debito = fields.Text(string="Abono", compute='_compute_payments')


