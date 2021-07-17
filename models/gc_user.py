from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    discord_uuid = fields.Char()
