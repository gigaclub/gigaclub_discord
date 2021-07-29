from odoo import fields, models, api


class GCDiscordCategory(models.Model):
    _name = 'gc.discord.category'
    _description = 'GigaClub Discord Category'

    name = fields.Char()
    discord_channel_uuid = fields.Char()
    channel_ids = fields.One2many(comodel_name="gc.discord.channel", inverse_name="category_id")
