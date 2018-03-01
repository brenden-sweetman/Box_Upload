from boxsdk import OAuth2
from boxsdk import Client
import requests
import time

clientID="pmg46vz4x71qkvxsg3p90r35q75s961q"
clientSecret="4gyRHY7qd9ttsukDnrJCp5gvKG97Dvw7"
#refreshToken="NpQE6mACg5eaCY5nYZsHzHBkg9f9BAan3x4MQdPFg7BqbuSZq2AciYaCizJqPWh2"
refreshToken=""
accessToken=""
expireTime=0
oauth = None
verbose=True

def refreshAuth():
    global clientID, clientSecret, refreshToken, accessToken, expireTime, startTime, verbose
    refreshPayload={
        'grant_type':'refresh_token',
        'refresh_token':refreshToken,
        'client_id':clientID,
        'client_secret':clientSecret}
    print refreshPayload
    response= requests.post("https://api.box.com/oauth2/token",refreshPayload)
    responseChunks= response.text.replace('{',"").replace('}',"").replace('\"',"").split(",")
    for s in responseChunks:
        chunks=s.split(":")
        if chunks[0]=="access_token":
            accessToken=chunks[1].replace(' ',"")
        if chunks[0]=="expires_in":
            expireTime= time.time()+int(chunks[1])
        if chunks[0]=="refresh_token":
            refreshToken=chunks[1]
    if verbose:
        print "Refresh Auth response:"
        print "Status: "+ str(response.status_code)
        print "Access Token: " +accessToken
        print "Refresh Token:" +refreshToken
        print "Access Token Experation:" + str(expireTime)
    writeCfg()

def writeCfg():
    global clientID, clientSecret, refreshToken, accessToken, expireTime
    with open("box.cfg", 'w') as cfg:
        cfg.write(clientID+"\n")
        cfg.write(clientSecret+"\n")
        cfg.write(refreshToken+"\n")
        cfg.write(accessToken+"\n")
        cfg.write(str(expireTime)+"\n")

def readCfg():
    global clientID, clientSecret, refreshToken, accessToken, expireTime
    with open ("box.cfg", 'r') as cfg:
        clientID= cfg.readline().replace("\n","")
        clientSecret= cfg.readline().replace("\n","")
        refreshToken= cfg.readline().replace("\n","")
        accessToken= cfg.readline().replace("\n","")
        expireTime= float(cfg.readline().replace("\n",""))

readCfg()
if expireTime<time.time():
    refreshAuth()
oauth= OAuth2(client_id=clientID,client_secret=clientSecret,access_token=accessToken)
client=Client(oauth)
root_items = client.folder(folder_id='0').get_items(limit=100,offset=0)
for item in root_items:
    print item["name"]
    print item["id"]
