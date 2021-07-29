from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    discord_uuid = fields.Char()

    _sql_constraints = [
        ("discord_uuid_unique", "UNIQUE(discord_uuid)", "DISCORD_UUID must be unique!")
    ]
