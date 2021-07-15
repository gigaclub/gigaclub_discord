import discord
import asyncio

from odoo import _, http
from odoo.http import request


class MainController(http.Controller):

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    client = discord.Client()

    @http.route(['/discordbot/start'], type="http", auth="public", method=['POST'], csrf=False)
    def start_discord_bot(self):
        config = request.env["res.config.settings"].search([("company_id", "=", request.env.user.company_id.id)],
                                                           limit=1)
        if config.gc_discord_bot_token and config.gc_discord_server_id and config.gc_discord_server_status == "stopped":
            self.loop.run_until_complete(self.client.start(config.gc_discord_bot_token))
        else:
            raise Exception(_("Bot is Started or Discord Bot Token or Discord Server ID not set!"))

    @http.route(['/discordbot/stop'], type="http", auth="public", method=['POST'], csrf=False)
    def stop_discord_bot(self):
        config = request.env["res.config.settings"].search([("company_id", "=", request.env.user.company_id.id)],
                                                           limit=1)
        if config.gc_discord_bot_token and config.gc_discord_server_id and config.gc_discord_server_status == "started":
            self.loop.run_until_complete(self.client.logout())
        else:
            raise Exception(_("Bot is Stopped or Discord Bot Token or Discord Server ID not set!"))

    @client.event
    async def on_ready(self):
        config = request.env["res.config.settings"].search([("company_id", "=", request.env.user.company_id.id)],
                                                           limit=1)
        config.gc_discord_server_status = "started"

    @client.event
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
