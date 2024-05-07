import requestBot as rb
import discord
from discord.ext import commands
import asyncio

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
    await ctx.send(rb.list())

@client.command()
async def serverOn(ctx):
    header = rb.getHeader()
    url = "https://mc.aubilius.tech/api/v2/servers"
    fetchServer = rb.getServer()
    availableServer = fetchServer['data']
    
    server_list_message = "Pilih server yang mau dinyalakan:\n"
    for index, server in enumerate(availableServer, start=1):
        server_list_message += f"{index}. {server['server_name']}\n"
    await ctx.send(server_list_message)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        user_input_message = await client.wait_for('message', timeout=10, check=check)

        selected_number = int(user_input_message.content)

        if 1 <= selected_number <= len(availableServer):
            selected_server = availableServer[selected_number - 1]
            await ctx.send(f"Anda telah memilih untuk menyalakan server: {selected_server['server_name']}")
            postingRequest = rb.session.post(url + f"/{selected_server['server_id']}/action/start_server", headers=header)
            status = postingRequest.json()['status']
            if postingRequest.status_code != 200:
                error = postingRequest.json()['error']
                await ctx.send(f"{status}\n{error}")
            else:
                await ctx.send(f"Berhasil menyalakan {selected_server['server_name']}: {status}")
        else:
            await ctx.send("Nomor server yang Anda masukkan tidak valid.")

    except asyncio.TimeoutError:
        await ctx.send("Waktu habis. Silakan coba lagi nanti.")

@client.command()
async def serverOff(ctx):
    header = rb.getHeader()
    url = "https://mc.aubilius.tech/api/v2/servers"
    fetchServer = rb.getServer()
    availableServer = fetchServer['data']
    
    server_list_message = "Pilih server yang mau dimatikan:\n"
    for index, server in enumerate(availableServer, start=1):
        server_list_message += f"{index}. {server['server_name']}\n"
    await ctx.send(server_list_message)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        user_input_message = await client.wait_for('message', timeout=10, check=check)

        selected_number = int(user_input_message.content)

        if 1 <= selected_number <= len(availableServer):
            selected_server = availableServer[selected_number - 1]
            await ctx.send(f"Anda telah memilih untuk mematikan server: {selected_server['server_name']}")
            postingRequest = rb.session.post(url + f"/{selected_server['server_id']}/action/stop_server", headers=header)
            status = postingRequest.json()['status']
            if postingRequest.status_code != 200:
                error = postingRequest.json()['error']
                await ctx.send(f"{status}\n{error}")
            else:
                await ctx.send(f"Berhasil mematikan {selected_server['server_name']}: {status}")
        else:
            await ctx.send("Nomor server yang Anda masukkan tidak valid.")

    except asyncio.TimeoutError:
        await ctx.send("Waktu habis. Silakan coba lagi nanti.")
        
client.run(rb.botToken)