from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    discord_uuid = fields.Char()
    role_ids = fields.Many2many(comodel_name="gc.discord.role")
    permission_profile_id = fields.Many2one(comodel_name="gc.discord.permission.profile")

    _sql_constraints = [
        ("discord_uuid_unique", "UNIQUE(discord_uuid)", "DISCORD_UUID must be unique!")
    ]
