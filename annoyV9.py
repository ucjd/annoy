import discord
import json
import requests
import os
import sys  # Import the sys module for exit()

# Ensure the 'download' directory exists
if not os.path.exists('download'):
    os.makedirs('download')

# Define your Discord bot token here
token = 'yourtokenhere'

os.system('cls')

header = {'authorization': token, 'x-super-properties': 'YOUR_SUPER_PROPERTIES_HERE'}

check_token = requests.get('https://discord.com/api/v9/users/@me', headers=header)

if check_token.status_code != 200:
    print('Invalid token, check config')
    sys.exit()  # Exit the script if the token is invalid

# Prompt the user for their Discord user ID
user = input("Enter the Discord ID of the user you want to annoy/reply to: ")

check_user = requests.get(f'https://discord.com/api/v9/users/{user}', headers=header)
check_user_response = json.loads(check_user.text)

username = check_user_response['username']
discriminator = check_user_response['discriminator']

client = discord.Client()

@client.event
async def on_message(message):
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

@client.event
async def on_connect():
    print(f'> Replying to {username}#{discriminator}')

client.run(token)
