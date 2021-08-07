import requests

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    gc_discord_bot_token = fields.Char(
        related="company_id.gc_discord_bot_token", readonly=False
    )
    gc_discord_server_id = fields.Char(
        related="company_id.gc_discord_server_id", readonly=False
    )
    gc_discord_system_channel_id = fields.Many2one(
        related="company_id.gc_discord_system_channel_id", readonly=False
    )
    gc_discord_reload = fields.Boolean(
        related="company_id.gc_discord_reload", readonly=False
    )
    gc_discord_server_status = fields.Selection(
        related="company_id.gc_discord_server_status"
    )

    def start_discord_bot(self):
        domain = self.env["ir.config_parameter"].get_param("web.base.url")
        requests.post(f"${domain}/discordbot/start")

    def stop_discord_bot(self):
        domain = self.env["ir.config_parameter"].get_param("web.base.url")
        requests.post(f"${domain}/discordbot/stop")

    def reload_bot(self):
        # self.ensure_one()
        # self.gc_discord_reload = True
        # requests.get("http://172.30.228.136:8080/reload")
        domain = self.env["ir.config_parameter"].get_param("web.base.url")
        requests.post(f"{domain}/discordbot/start")
