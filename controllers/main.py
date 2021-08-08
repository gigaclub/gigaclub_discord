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
