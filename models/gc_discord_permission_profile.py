from odoo import fields, models, api


class GCDiscordPermissionProfile(models.Model):
    _name = 'gc.discord.permission.profile'
    _description = 'GigaClub Discord Permission Profile'

    name = fields.Char()

    administrator = fields.Boolean()
    create_instant_invite = fields.Boolean()
    kick_members = fields.Boolean()
    ban_members = fields.Boolean()
    manage_channels = fields.Boolean()
    manage_guild = fields.Boolean()
    add_reactions = fields.Boolean()
    view_audit_log = fields.Boolean()
    priority_speaker = fields.Boolean()
    stream = fields.Boolean()
    read_messages = fields.Boolean()
    send_messages = fields.Boolean()
    send_tts_messages = fields.Boolean()
    manage_messages = fields.Boolean()
    embed_links = fields.Boolean()
    attach_files = fields.Boolean()
    read_message_history = fields.Boolean()
    mention_everyone = fields.Boolean()
    external_emojis = fields.Boolean()
    view_guild_insights = fields.Boolean()
    connect = fields.Boolean()
    speak = fields.Boolean()
    mute_members = fields.Boolean()
    deafen_members = fields.Boolean()
    move_members = fields.Boolean()
    use_voice_activation = fields.Boolean()
    change_nickname = fields.Boolean()
    manage_nicknames = fields.Boolean()
    manage_roles = fields.Boolean()
    manage_webhooks = fields.Boolean()
    manage_emojis = fields.Boolean()
    use_slash_commands = fields.Boolean()
    request_to_speak = fields.Boolean()
