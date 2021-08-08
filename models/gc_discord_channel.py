from odoo import fields, models, api


class GCDiscordChannel(models.Model):
    _name = 'gc.discord.channel'
    _description = 'GigaClub Discord Channel'

    name = fields.Char()
    discord_channel_uuid = fields.Char(readonly=True)
    type = fields.Selection(
        selection=[
            ("text", "Text"),
            ("voice", "Voice"),
            ("stage", "Stage"),
            ("announcement", "Announcement")
        ]
    )
    category_id = fields.Many2one(comodel_name="gc.discord.category")
    permission_profile_id = fields.Many2one(comodel_name="gc.discord.permission.profile")


