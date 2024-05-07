import requests as req
import json
import asyncio


file = open('config.json')
jsonData = json.load(file)
credentials = jsonData['data']
botToken = jsonData['token']
session = req.Session()
url = "https://mc.aubilius.tech/api/v2/auth/login"

def giveBotToken():
    return botToken

def getToken():
    login = session.post(url, json=credentials)
    response = login.json()
    token = response['data']['token']
    return token

def getHeader():
    token = getToken()
    header = {"Authorization": f"{token}"}
    return header

def getServer():
    header = getHeader()
    url = "https://mc.aubilius.tech/api/v2/servers"
    listServer = session.get(url, headers=header)
    response = listServer.content
    jsonServer = json.loads(response)
    return jsonServer

def list():
    header = getHeader()
    url = "https://mc.aubilius.tech/api/v2/servers"
    fetchServer = getServer()
    
    serverDetail = fetchServer['data']
    message = "## Halo! Ini Informasi server yang kamu minta:\n\n>>> "
    for item in serverDetail:
        serverId = item['server_id']
        serverName = item['server_name']
        doStatsReq = session.get(url + f"/{serverId}/stats", headers=header)
        content = doStatsReq.content
        serverInfo = json.loads(content)
        
        runStats = serverInfo['data']['running']
        
        if runStats == True:
            message += f"Server ID: {serverId}\nServer Name: {serverName}\nServer Status: ```diff\n! Online\n```\n"
        else:
            message += f"Server ID: {serverId}\nServer Name: {serverName}\nServer Status: ```diff\n- Offline\n```\n"
    return message



