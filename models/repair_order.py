from odoo import models, fields, api
from odoo.exceptions import UserError

class RepairOrder(models.Model):
    _inherit = "repair.order"

    workorder_ids = fields.One2many(
        "repair.workorder",
        "repair_id",
        string="Operations"
    )

    def action_confirm(self):
        res = super().action_confirm()
        for repair in self:
            if not repair.workorder_ids:
                raise UserError("Você precisa criar pelo menos uma operação antes de confirmar.")
        return res

    def action_repair_done(self):
        for repair in self:
            if any(wo.state != 'done' for wo in repair.workorder_ids):
                raise UserError("Existem operações não finalizadas.")
        return super().action_repair_done()
