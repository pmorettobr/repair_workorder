from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class RepairWorkorder(models.Model):
    _name = "repair.workorder"
    _description = "Repair Work Order"
    _order = "sequence, id"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    repair_id = fields.Many2one(
        "repair.order",
        required=True,
        ondelete="cascade"
    )

    workcenter_id = fields.Many2one(
        "mrp.workcenter",
        string="Work Center",
        required=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('done', 'Done')
    ], default='draft')

    time_ids = fields.One2many(
        "repair.workorder.time",
        "workorder_id",
        string="Time Logs"
    )

    duration = fields.Float(
        compute="_compute_duration",
        store=True
    )

    current_employee_id = fields.Many2one(
        "hr.employee",
        compute="_compute_current_employee",
        string="Current Operator"
    )

    is_workcenter_busy = fields.Boolean(
        compute="_compute_workcenter_busy",
        string="Machine Busy"
    )

    display_time = fields.Char(
        compute="_compute_display_time",
        string="Timer"
    )

    @api.depends("time_ids.duration")
    def _compute_duration(self):
        for rec in self:
            rec.duration = sum(rec.time_ids.mapped("duration"))

    @api.depends("time_ids")
    def _compute_current_employee(self):
        for rec in self:
            open_log = rec.time_ids.filtered(lambda t: not t.date_end)
            rec.current_employee_id = open_log.employee_id.id if open_log else False

    @api.depends("workcenter_id", "state")
    def _compute_workcenter_busy(self):
        for rec in self:
            busy = self.search([
                ('workcenter_id','=', rec.workcenter_id.id),
                ('state','=','progress'),
                ('id','!=', rec.id)
            ])
            rec.is_workcenter_busy = bool(busy)

    @api.depends("time_ids.date_start", "time_ids.date_end", "state")
    def _compute_display_time(self):
        for rec in self:
            open_log = rec.time_ids.filtered(lambda t: not t.date_end)
            if open_log:
                delta = datetime.now() - open_log.date_start
                hours, rem = divmod(delta.total_seconds(), 3600)
                minutes, seconds = divmod(rem, 60)
                rec.display_time = "%02d:%02d:%02d" % (hours, minutes, seconds)
            else:
                rec.display_time = "00:00:00"

    def action_start(self):
        if self.repair_id.state != 'confirmed':
            raise UserError("Só é possível iniciar a operação após o Repair ser confirmado.")
        if self.is_workcenter_busy:
            raise UserError("Esta máquina já está em uso.")
        self.state = 'progress'
        self.env["repair.workorder.time"].create({
            "workorder_id": self.id,
            "employee_id": self.env.user.employee_id.id,
            "date_start": fields.Datetime.now(),
        })

    def action_done(self):
        open_time = self.time_ids.filtered(lambda t: not t.date_end)
        if open_time:
            open_time.write({"date_end": fields.Datetime.now()})
        self.state = 'done'
