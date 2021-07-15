from odoo import _, fields, models
import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gc_discord_bot_token = fields.Char(related="company_id.gc_discord_bot_token", readonly=False)
    gc_discord_server_id = fields.Char(related="company_id.gc_discord_server_id", readonly=False)
    gc_discord_server_status = fields.Selection(related="company_id.gc_discord_server_status")

    def start_discord_bot(self):
        domain = self.env['ir.config_parameter'].get_param('web.base.url')
        requests.post(f"${domain}/discordbot/start")

    def stop_discord_bot(self):
        domain = self.env['ir.config_parameter'].get_param('web.base.url')
        requests.post(f"${domain}/discordbot/stop")
