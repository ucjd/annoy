import discord
import json
import aiohttp
import os
import sys

# Ensure the 'download' directory exists
if not os.path.exists('download'):
    os.makedirs('download')

# Define your Discord user token here (selfbot token)
token = 'OTAxNTEyMDAzMTI5MDYxMzg3.Gh2nNR.sdIUmKbHY03oWapr2woIfafi-AhW-lOHoCucSY'
api_url = 'https://discord.com/api/v9'

headers = {'authorization': token}

async def check_token_validity():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{api_url}/users/@me', headers=headers) as response:
            return response.status == 200

async def get_user_info(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{api_url}/users/{user_id}', headers=headers) as response:
            return await response.json()

class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author.id == int(user):
            if message.attachments:
                for attachment in message.attachments:
                    # Save the attachment
                    await attachment.save(f'download/{attachment.filename}')
                    print(f'> Saved File > {attachment.filename}')

                    # Send the attachment
                    await message.channel.send(file=discord.File(f'download/{attachment.filename}'))
                    print(f'> Sent File > {attachment.filename}')

                    # Delete the file after sending
                    os.remove(f'download/{attachment.filename}')
                    print(f'> Deleted File > {attachment.filename}')

            if message.embeds:
                for embed in message.embeds:
                    if embed.type == 'image' or embed.type == 'video':
                        # Send the embedded image or video back
                        await message.channel.send(embed.url)
                        print(f'> Sent Embedded Image/Video > {embed.url}')

            if message.content.strip():  # Check if the message content is not empty
                # Send the text content
                await message.channel.send(message.content)
                print(f'> Sent > {message.content}')

    async def on_connect(self):
        user_info = await get_user_info(user)
        global username, discriminator
        username = user_info['username']
        discriminator = user_info['discriminator']
        print(f'> Replying to {username}#{discriminator}')

async def main():
    if not await check_token_validity():
        print('Invalid token, check config')
        sys.exit()

    # Prompt the user for their Discord user ID
    global user
    user = input("Enter the Discord ID of the user you want to annoy/reply to: ")

    client = MyClient()
    await client.start(token)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
