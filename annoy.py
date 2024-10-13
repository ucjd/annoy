import discord
import json
import aiohttp
import os
import sys
import asyncio
from discord.ext import commands
from aiohttp import ClientSession

if not os.path.exists('download'):
    os.makedirs('download')

token = 'yourtokenhere'

os.system('cls')

header = {'authorization': token}

async def check_token():
    async with ClientSession() as session:
        async with session.get('https://discord.com/api/v9/users/@me', headers=header) as response:
            return response.status == 200

async def main():
    if not await check_token():
        print('Invalid token, check config')
        sys.exit()

    user = input("Enter the Discord ID of the user you want to annoy/reply to: ")

    async def check_user():
        async with ClientSession() as session:
            async with session.get(f'https://discord.com/api/v9/users/{user}', headers=header) as response:
                return await response.json()

    check_user_response = await check_user()

    username = check_user_response['username']
    discriminator = check_user_response['discriminator']

    client = commands.Bot(command_prefix="!")

    @client.event
    async def on_message(message):
        if message.author.id == int(user):
            if message.attachments:
                for attachment in message.attachments:
                    await attachment.save(f'download/{attachment.filename}')
                    await message.channel.send(file=discord.File(f'download/{attachment.filename}'))
                    os.remove(f'download/{attachment.filename}')

            if message.embeds:
                for embed in message.embeds:
                    if embed.type == 'image' or embed.type == 'video':
                        await message.channel.send(embed.url)

            if message.content.strip():
                await message.channel.send(message.content)

    @client.event
    async def on_connect():
        print(f'> Replying to {username}#{discriminator}')

    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
