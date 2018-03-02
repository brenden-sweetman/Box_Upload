#!/usr/bin/env python
# Author: Brenden Sweetman brenden.sweetman@wustl.edu
# Title reauth.py
# Purpose: Generate initial access and refresh tokens for a new user of box_upload.py

import requests
import re
import time

print "This Script Authenticates the box_upload.py application to access your box account"
print "Enter your client ID:"
clientID=raw_input()
print "Enter your client secret"
clientSecret=raw_input()
print "Type the following url into a browser login to your account and paste the code generated below"
print "https://account.box.com/api/oauth2/authorize?response_type=code&client_id="+clientID
code=raw_input()
# Prepare payload
payload={
    "grant_type":"authorization_code",
    "code":code,
    "client_id":clientID,
    "client_secret":clientSecret
}
# Make token request
response = requests.post("https://api.box.com/oauth2/token",payload)
if response.status_code==200:
    accessToken= re.findall(r"access_token\":\"([^\"]+)\"",response.text)[0]
    refreshToken= re.findall(r"refresh_token\":\"([^\"]+)\"",response.text)[0]
    expireTime= int(re.findall(r"expires_in\":(\d+)",response.text)[0])+ time.time()
# print error if bad request
else: print "Access Token could not be created."
# write a config file will full access token
with open("box_initial.cfg", 'w') as cfg:
    cfg.write(clientID+"\n")
    cfg.write(clientSecret+"\n")
    cfg.write(refreshToken+"\n")
    cfg.write(accessToken+"\n")
    cfg.write(str(expireTime)+"\n")
