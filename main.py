import discord
from discord.ext import commands
import requests as req
import json
import os
import asyncio

url = "https://mc.aubilius.tech/api/v2/auth/login"
data = {
    'username' : '<crafty_username>',
    'password' : '<crafty_password>'
}
session = req.Session()
doLogin = session.post(url, json=data)
token_key = doLogin.json()['data']['token']


intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix= '!')

@client.event
async def on_ready():
    text = "Bot are settled up"
    print(text)
    print("="*len(text))
    
@client.command()
async def man(ctx):
    helpString = """
    ```Prefixnya '!' ya, di bawah ini list command yang udah ada:\nCommand\n- !list\n- !serverOn\n- !serverOff```"""
    await ctx.send(helpString)
@client.command()
async def list(ctx):
    header = {"Authorization": f"{token_key}"}
    url = "https://mc.aubilius.tech/api/v2/servers"
    doRequest = session.get(url, headers=header)
    
    content = doRequest.content
    parsedData = json.loads(content)

    message = "## Halo! Ini Informasi server yang kamu minta:\n\n>>> "
    serversDetail = parsedData['data']
    for item in serversDetail:
        server_id = item['server_id']
        server_name = item['server_name']
        message += f'Server ID: {server_id}\nServer Name: {server_name}\n\n'

    await ctx.send(f'{message}')
    
@client.command()
async def serverOn(ctx):
    # Get the list of available servers (assuming you have it stored somewhere)
    header = {"Authorization": f"{token_key}"}
    url = "https://mc.aubilius.tech/api/v2/servers"
    doRequest = session.get(url, headers=header)
    
    content = doRequest.content
    parsed_data = json.loads(content)
    available_servers = parsed_data['data']

    # Display the list of available servers with numbering
    server_list_message = "Pilih server yang mau dinyalakan:\n"
    for index, server in enumerate(available_servers, start=1):
        server_list_message += f"{index}. {server['server_name']}\n"
    await ctx.send(server_list_message)

    def check(message):
        # Define a function to check if the message is from the same user and in the same channel
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Wait for a message from the same user and in the same channel
        # with a timeout of 60 seconds
        user_input_message = await client.wait_for('message', timeout=60, check=check)

        # Process the user's input message
        selected_number = int(user_input_message.content)

        # Validate the selected number
        if 1 <= selected_number <= len(available_servers):
            selected_server = available_servers[selected_number - 1]
            await ctx.send(f"Anda telah memilih untuk menyalakan server: {selected_server['server_name']}")
            postingRequest = session.post(url + f"/{selected_server['server_id']}/action/start_server", headers=header)
            status = postingRequest.json()['status']
            if postingRequest.status_code != 200:
                error = postingRequest.json()['error']
                await ctx.send(f"{status}\n{error}")
            else:
                await ctx.send(f"Berhasil menyalakan {selected_server['server_name']}: {status}")
            # Add more code here to handle turning on the selected server
            # You can access the server ID using selected_server['server_id']
        else:
            await ctx.send("Nomor server yang Anda masukkan tidak valid.")

    except asyncio.TimeoutError:
        # If the user doesn't respond within 60 seconds, handle the timeout
        await ctx.send("Waktu habis. Silakan coba lagi nanti.")
        
        
@client.command()
async def serverOff(ctx):
    # Get the list of available servers (assuming you have it stored somewhere)
    header = {"Authorization": f"{token_key}"}
    url = "https://mc.aubilius.tech/api/v2/servers"
    doRequest = session.get(url, headers=header)
    
    content = doRequest.content
    parsed_data = json.loads(content)
    available_servers = parsed_data['data']

    # Display the list of available servers with numbering
    server_list_message = "Pilih server yang mau dimatikan:\n"
    for index, server in enumerate(available_servers, start=1):
        server_list_message += f"{index}. {server['server_name']}\n"
    await ctx.send(server_list_message)

    def check(message):
        # Define a function to check if the message is from the same user and in the same channel
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Wait for a message from the same user and in the same channel
        # with a timeout of 60 seconds
        user_input_message = await client.wait_for('message', timeout=60, check=check)

        # Process the user's input message
        selected_number = int(user_input_message.content)

        # Validate the selected number
        if 1 <= selected_number <= len(available_servers):
            selected_server = available_servers[selected_number - 1]
            await ctx.send(f"Anda telah memilih untuk mematikan server: {selected_server['server_name']}")
            postingRequest = session.post(url + f"/{selected_server['server_id']}/action/stop_server", headers=header)
            status = postingRequest.json()['status']
            if postingRequest.status_code != 200:
                error = postingRequest.json()['error']
                await ctx.send(f"{status}\n{error}")
            else:
                await ctx.send(f"Berhasil mematikan {selected_server['server_name']}: {status}")
            # Add more code here to handle turning on the selected server
            # You can access the server ID using selected_server['server_id']
        else:
            await ctx.send("Nomor server yang Anda masukkan tidak valid.")

    except asyncio.TimeoutError:
        # If the user doesn't respond within 60 seconds, handle the timeout
        await ctx.send("Waktu habis. Silakan coba lagi nanti.")

client.run('token')    
