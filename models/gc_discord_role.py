from odoo import fields, models, api


class GCDiscordRole(models.Model):
    _name = 'gc.discord.role'
    _description = 'GigaClub Discord Role'

    name = fields.Char()
