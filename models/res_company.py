from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    gc_discord_bot_token = fields.Char("Discord Bot Token")
    gc_discord_server_id = fields.Char("Discord Server ID")
