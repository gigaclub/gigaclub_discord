from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gc_discord_bot_token = fields.Char(related="company_id.gc_discord_bot_token")
    gc_discord_server_id = fields.Char(related="company_id.gc_discord_server_id")
