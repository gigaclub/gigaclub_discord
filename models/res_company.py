from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    gc_discord_bot_token = fields.Char("Discord Bot Token")
    gc_discord_server_id = fields.Char("Discord Server ID")
    gc_discord_bot_status = fields.Selection(
        [
            ("started", "Started"),
            ("stopped", "Stopped"),
        ],
        default="stopped",
    )