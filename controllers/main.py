from discord.ext import commands
import discord
import asyncio
import threading

from odoo import _, http, api, registry
from odoo.http import request


class MainController(http.Controller):
    class MyBot(commands.Bot):
        def __init__(self, command_prefix, env):
            commands.Bot.__init__(self, command_prefix=command_prefix)
            self.env = env

        async def on_ready(self):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    company_id = new_env.user.company_id or new_env["res.company"].browse(1)
                    company_id.gc_discord_server_status = "started"
                    for guild in self.guilds:
                        if not new_env["gc.user"].search_count([("discord_uuid", "=", str(guild.owner_id))]):
                            new_env["gc.user"].create({"discord_uuid": str(guild.owner_id)})
                        for member in guild.members:
                            if not new_env["gc.user"].search_count([("discord_uuid", "=", str(member.id))]):
                                new_env["gc.user"].create({"discord_uuid": str(member.id)})
                        for channel in guild.channels:
                            if isinstance(channel, discord.channel.CategoryChannel):
                                await self.register_category(channel)
                            else:
                                await self.register_channel(channel)
                        for role in guild.roles:
                            await self.register_role(role)

        async def register_role(self, role):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.discord.role"].search_count([("role_id", "=", str(role.id))]):
                        role_id = new_env["gc.discord.role"].create({
                            "name": role.name,
                            "role_id": str(role.id),
                            "hoist": role.hoist,
                            "position": role.position,
                            "managed": role.managed,
                            "mentionable": role.mentionable
                        })
                        member_ids = []
                        for member in role.members:
                            user_id = new_env["gc.user"].search([("discord_uuid", "=", str(member.id))], limit=1)
                            if user_id:
                                member_ids.append(user_id.id)
                        role_id.user_ids = [[6, 0, member_ids]]
                        permission_profile_id = role_id.permission_profile_id.create({
                            "name": role.name,
                            "administrator": role.permissions.administrator,
                            "create_instant_invite": role.permissions.create_instant_invite,
                            "kick_members": role.permissions.kick_members,
                            "ban_members": role.permissions.ban_members,
                            "manage_channels": role.permissions.manage_channels,
                            "manage_guild": role.permissions.manage_guild,
                            "add_reactions": role.permissions.add_reactions,
                            "view_audit_log": role.permissions.view_audit_log,
                            "priority_speaker": role.permissions.priority_speaker,
                            "stream": role.permissions.stream,
                            "read_messages": role.permissions.read_messages,
                            "send_messages": role.permissions.send_messages,
                            "send_tts_messages": role.permissions.send_tts_messages,
                            "manage_messages": role.permissions.manage_messages,
                            "embed_links": role.permissions.embed_links,
                            "attach_files": role.permissions.attach_files,
                            "read_message_history": role.permissions.read_message_history,
                            "mention_everyone": role.permissions.mention_everyone,
                            "external_emojis": role.permissions.external_emojis,
                            "view_guild_insights": role.permissions.view_guild_insights,
                            "connect": role.permissions.connect,
                            "speak": role.permissions.speak,
                            "mute_members": role.permissions.mute_members,
                            "deafen_members": role.permissions.deafen_members,
                            "move_members": role.permissions.move_members,
                            "use_voice_activation": role.permissions.use_voice_activation,
                            "change_nickname": role.permissions.change_nickname,
                            "manage_nicknames": role.permissions.manage_nicknames,
                            "manage_roles": role.permissions.manage_roles,
                            "manage_webhooks": role.permissions.manage_webhooks,
                            "manage_emojis": role.permissions.manage_emojis,
                            "use_slash_commands": role.permissions.use_slash_commands,
                            "request_to_speak": role.permissions.request_to_speak
                        })
                        role_id.permission_profile_id = permission_profile_id
                    else:
                        role_id = new_env["gc.discord.role"].search([("role_id", "=", str(role.id))], limit=1)
                        permissions = discord.Permissions(
                            administrator=role_id.permission_profile_id.administrator,
                            create_instant_invite=role_id.permission_profile_id.create_instant_invite,
                            kick_members=role_id.permission_profile_id.kick_members,
                            ban_members=role_id.permission_profile_id.ban_members,
                            manage_channels=role_id.permission_profile_id.manage_channels,
                            manage_guild=role_id.permission_profile_id.manage_guild,
                            add_reactions=role_id.permission_profile_id.add_reactions,
                            view_audit_log=role_id.permission_profile_id.view_audit_log,
                            priority_speaker=role_id.permission_profile_id.priority_speaker,
                            stream=role_id.permission_profile_id.stream,
                            read_messages=role_id.permission_profile_id.read_messages,
                            send_messages=role_id.permission_profile_id.send_messages,
                            send_tts_messages=role_id.permission_profile_id.send_tts_messages,
                            manage_messages=role_id.permission_profile_id.manage_messages,
                            embed_links=role_id.permission_profile_id.embed_links,
                            attach_files=role_id.permission_profile_id.attach_files,
                            read_message_history=role_id.permission_profile_id.read_message_history,
                            mention_everyone=role_id.permission_profile_id.mention_everyone,
                            external_emojis=role_id.permission_profile_id.external_emojis,
                            view_guild_insights=role_id.permission_profile_id.view_guild_insights,
                            connect=role_id.permission_profile_id.connect,
                            speak=role_id.permission_profile_id.speak,
                            mute_members=role_id.permission_profile_id.mute_members,
                            deafen_members=role_id.permission_profile_id.deafen_members,
                            move_members=role_id.permission_profile_id.move_members,
                            use_voice_activation=role_id.permission_profile_id.use_voice_activation,
                            change_nickname=role_id.permission_profile_id.change_nickname,
                            manage_nicknames=role_id.permission_profile_id.manage_nicknames,
                            manage_roles=role_id.permission_profile_id.manage_roles,
                            manage_webhooks=role_id.permission_profile_id.manage_webhooks,
                            manage_emojis=role_id.permission_profile_id.manage_emojis,
                            use_slash_commands=role_id.permission_profile_id.use_slash_commands,
                            request_to_speak=role_id.permission_profile_id.request_to_speak
                        )
                        await role.edit(
                            name=role_id.name,
                            hoist=role_id.hoist,
                            mentionable=role_id.mentionable,
                            position=role_id.position,
                            permissions=permissions
                        )


        async def register_category(self, channel):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.discord.category"].search_count([("discord_channel_uuid", "=", str(channel.id))]):
                        new_env["gc.discord.category"].create({
                            "discord_channel_uuid": str(channel.id),
                            "name": str(channel.name)
                        })
                    else:
                        category_id = new_env["gc.discord.category"].search([("discord_channel_uuid", "=", str(channel.id))])
                        await channel.edit(name=category_id.name)

        async def register_channel(self, channel):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.discord.channel"].search_count([("discord_channel_uuid", "=", str(channel.id))]):
                        type = False
                        if isinstance(channel, discord.channel.TextChannel):
                            type = "text"
                            if channel.is_news():
                                type = "announcement"
                        elif isinstance(channel, discord.channel.VoiceChannel):
                            type = "voice"
                        elif isinstance(channel, discord.channel.StageChannel):
                            type = "stage"
                        if type:
                            create_dict = {
                                "discord_channel_uuid": str(channel.id),
                                "name": str(channel.name),
                                "type": type
                            }
                            if channel.category:
                                await self.register_category(channel.category)
                                category_id = new_env["gc.discord.category"].search(
                                    [("discord_channel_uuid", "=", str(channel.category.id))])
                                if category_id:
                                    create_dict["category_id"] = category_id.id
                            new_env["gc.discord.channel"].create(create_dict)
                    else:
                        channel_id = new_env["gc.discord.channel"].search([("discord_channel_uuid", "=", str(channel.id))])
                        if channel_id:
                            await channel.edit(name=channel_id.name)
                            if channel_id.category_id:
                                category = self.get_channel(int(channel_id.category_id.discord_channel_uuid))
                                await channel.edit(category=category)
                            else:
                                await channel.edit(category=None)

        async def refresh_categories_and_channels(self):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    company_id = new_env.user.company_id or new_env["res.company"].browse(1)
                    if company_id.gc_discord_reload:
                        for guild in self.guilds:
                            if guild.id == int(company_id.gc_discord_server_id):
                                for role in guild.roles:
                                    await self.register_role(role)
                                for channel in guild.channels:
                                    if isinstance(channel, discord.channel.CategoryChannel):
                                        await self.register_category(channel)
                                    else:
                                        await self.register_channel(channel)
                                    not_created_channel_ids = new_env["gc.discord.channel"].search([("discord_channel_uuid", "=", False)])
                                    if not_created_channel_ids:
                                        for channel_id in not_created_channel_ids:
                                            category = False
                                            channel = False
                                            if channel_id.category_id and not channel_id.category_id.discord_channel_uuid:
                                                category = await guild.create_category(name=channel_id.category_id.name)
                                                channel_id.category_id.discord_channel_uuid = str(category.id)
                                            elif channel_id.category_id:
                                                category = await guild.get_channel(int(channel_id.category_id.discord_channel_uuid))
                                            if channel_id.type == "text":
                                                channel = await guild.create_text_channel(name=channel_id.name, category=category)
                                            elif channel_id.type == "voice":
                                                channel = await guild.create_voice_channel(name=channel_id.name, category=category)
                                            elif channel_id.type == "stage":
                                                channel = await guild.create_stage_channel(name=channel_id.name, category=category)
                                            elif channel_id.type == "announcement":
                                                channel = await guild.create_text_channel(name=channel_id.name, category=category, type=discord.ChannelType.news)
                                            new_env["gc.discord.channel"].write({"discord_channel_uuid": str(channel.id)})
                                    not_created_category_ids = new_env["gc.discord.category"].search([("discord_channel_uuid", "=", False)])
                                    if not_created_category_ids:
                                        for category_id in not_created_category_ids:
                                            category = await guild.create_category(name=category_id.name)
                                            category_id.discord_channel_uuid = str(category.id)

        async def on_message(self, message):
            if message.author == self.user:
                return

            if message.content.startswith('$hello'):
                await message.channel.send('Hello!')

        async def shutdown(self):
            await self.logout()

    async def bot_async_start(self, gc_discord_bot_token):
        await self.client.start(gc_discord_bot_token)

    def bot_loop_start(self, loop):
        loop.run_forever()

    @http.route(['/discordbot/start'], type="http", method=['POST'], csrf=False)
    def start_discord_bot(self):
        company_id = request.env.user.company_id or request.env["res.company"].browse(1)
        if company_id.gc_discord_bot_token and company_id.gc_discord_server_status and company_id.gc_discord_server_status == "stopped":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.client = self.MyBot(command_prefix="!", env=request.env)
            loop.create_task(self.bot_async_start(company_id.gc_discord_bot_token))
            bot_thread = threading.Thread(target=self.bot_loop_start, args=(loop,))
            bot_thread.start()
        else:
            raise Exception(_("Bot is Started or Discord Bot Token or Discord Server ID not set!"))
        return "<script>window.close()</script>"

    @http.route(['/discordbot/stop'], type="http", method=['POST'], csrf=False)
    def stop_discord_bot(self):
        company_id = request.env.user.company_id or request.env["res.company"].browse(1)
        if company_id.gc_discord_bot_token and company_id.gc_discord_server_status and company_id.gc_discord_server_status == "started":
            try:
                asyncio.run(self.client.logout())
                del self.client
            except:
                pass
            company_id.gc_discord_server_status = "stopped"
        else:
            raise Exception(_("Bot is Stopped or Discord Bot Token or Discord Server ID not set!"))
        return "<script>window.close()</script>"

    @http.route(["/discordbot/reload"], type="http", method=["POST"], csrf=False)
    def reload_discord_bot(self):
        self.stop_discord_bot()
        self.start_discord_bot()
        asyncio.run(self.client.refresh_categories_and_channels())
        return "<script>window.close()</script>"
