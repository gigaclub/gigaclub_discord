from odoo import fields, models, api


class GCDiscordRole(models.Model):
    _name = 'gc.discord.role'
    _description = 'GigaClub Discord Role'

    name = fields.Char()
    role_id = fields.Integer()
    hoist = fields.Boolean()
    position = fields.Integer()
    managed = fields.Boolean()
    mentionable = fields.Boolean()

    user_ids = fields.Many2many(comodel_name="gc.user")
    permission_profile_id = fields.Many2one(comodel_name="gc.discord.permission.profile")
