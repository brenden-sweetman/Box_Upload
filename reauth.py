import requests

#request url: https://account.box.com/api/oauth2/authorize?response_type=code&client_id=pmg46vz4x71qkvxsg3p90r35q75s961q

def writeCfg():
    global clientID, clientSecret, refreshToken, accessToken, expireTime
    with open("box.cfg", 'w') as cfg:
        cfg.write(clientID+"\n")
        cfg.write(clientSecret+"\n")
        cfg.write(refreshToken+"\n")
        cfg.write(accessToken+"\n")
        cfg.write(str(expireTime)+"\n")




request= requests.post("https://api.box.com/oauth2/token", {"grant_type":"authorization_code","code":"KON9I7idVGLUwjvFnukqjFhngVfo6md3","client_id":"pmg46vz4x71qkvxsg3p90r35q75s961q","client_secret":"4gyRHY7qd9ttsukDnrJCp5gvKG97Dvw7"})
print request.text
