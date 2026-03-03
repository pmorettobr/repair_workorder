from odoo import models, fields, api

class RepairWorkorderTime(models.Model):
    _name = "repair.workorder.time"
    _description = "Repair Workorder Time Log"

    workorder_id = fields.Many2one(
        "repair.workorder",
        required=True,
        ondelete="cascade"
    )

    employee_id = fields.Many2one(
        "hr.employee",
        required=True
    )

    date_start = fields.Datetime(required=True)
    date_end = fields.Datetime()

    duration = fields.Float(
        compute="_compute_duration",
        store=True
    )

    @api.depends("date_start", "date_end")
    def _compute_duration(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                delta = rec.date_end - rec.date_start
                rec.duration = delta.total_seconds() / 3600
            else:
                rec.duration = 0.0
