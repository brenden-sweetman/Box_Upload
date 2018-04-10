#!/usr/bin/env python3
# Author: Brenden Sweetman brenden.sweetman@wustl.edu
# Title reauth.py
# Purpose: Generate initial access and refresh tokens for a new user of box_upload.py
#   The box api requires that any application get initial password permission for
#   any user that will use the application functionality. In our case there only
#   needs to be one user that is authorized with the app. This script can be used
#   to change the user authorized with the application at any time

import requests
import re
import time
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="A script to create initial access token for box_upload.")
    parser.add_argument("-i","--client_id",help="client id from box developer", type=str, required=True)
    parser.add_argument("-f","--file_name",help="name of config file to save without extension", type=str , required=True)
    args=parser.parse_args(sys.argv[1:])
    clientID= args.client_id
    fileName= args.file_name
    # request client secret
    print ("Type your client secret: ")
    clientSecret= input()
    # request user to authenticate
    print ("Type the following url into a browser, login to your account, and paste the code generated in the url\n This must be done in 30 seconds\n If you don't know what the code is please refer to the technical documentation")
    print ("https://account.box.com/api/oauth2/authorize?response_type=code&client_id="+clientID)
    # get auth code from user
    code=input()
    # Prepare payload
    payload={
        "grant_type":"authorization_code",
        "code":code,
        "client_id":clientID,
        "client_secret":clientSecret
    }
    # Make token request
    response = requests.post("https://api.box.com/oauth2/token",payload)
    # Parse token request and save results to file
    if response.status_code==200:
        accessToken= re.findall(r"access_token\":\"([^\"]+)\"",response.text)[0]
        refreshToken= re.findall(r"refresh_token\":\"([^\"]+)\"",response.text)[0]
        expireTime= int(re.findall(r"expires_in\":(\d+)",response.text)[0])+ time.time()
        # write a config file will full access token
        with open(fileName+".cfg", 'w') as cfg:
            cfg.write(clientID+"\n")
            cfg.write(clientSecret+"\n")
            cfg.write(refreshToken+"\n")
            cfg.write(accessToken+"\n")
            cfg.write(str(expireTime)+"\n")
    # print error if bad request
    else: print ("Access Token could not be created.")

if __name__=="__main__":
     main()
