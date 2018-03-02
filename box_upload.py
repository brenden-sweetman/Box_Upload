#!/usr/bin/env python
from boxsdk import OAuth2
from boxsdk import Client
from boxsdk import exception
import requests
import time
import re
import sys , os
import ntpath
import argparse
from StringIO import StringIO

clientID=""
clientSecret=""
refreshToken=""
accessToken=""
expireTime=0
# ID for folder to upload files
folderID=46200064078
oauth = None
client = None
verbose= False


### Main function ###
def main():
    global client, oauth, verbose
    #parse command line arguments
    parser = argparse.ArgumentParser(description="Upload File to box")
    parser.add_argument("-v","--verbose", help="activate verbose mode", action='store_true')
    parser.add_argument("-f","--file", help="path to upload file", type=str, required=True)
    args=parser.parse_args(sys.argv[1:])
    verbose=args.verbose
    # read config
    readCfg()
    # updtae auth if needed
    if expireTime<time.time():
        refreshAuth()
        writeCfg()
    # Autenticate with box
    oauth= OAuth2(client_id=clientID,client_secret=clientSecret,access_token=accessToken)
    # Create client
    client=Client(oauth)
    # Upload file
    upload(args.file)

def upload(filePath,folder=folderID):
    global client, verbose
    try:
        print "Starting Upload to box...\n\n"
        box_file=client.folder(str(folder)).upload(filePath,ntpath.basename(filePath))
        if verbose:
            print "Uploaded file to box"
            print "File Name: "+ box_file.name
            print "File ID: " + box_file.id
            print "In Folder:"
            print "\tName: " + client.folder(str(folder)).get()['name']
            print "\tID: " + str(folder)
    except exception.BoxAPIException as e:
        print "Error uploading file: " + e.message

def refreshAuth():
    global clientID, clientSecret, refreshToken, accessToken, expireTime , folderID, verbose
    ### Request Global Acess Token ###
    # prepare authentication request (see: https://developer.box.com/reference#oauth-2-overview)
    refreshPayload={
        'grant_type':'refresh_token',
        'refresh_token':refreshToken,
        'client_id':clientID,
        'client_secret':clientSecret}
    # send post request
    response= requests.post("https://api.box.com/oauth2/token",refreshPayload)
    # parse response
    if response.status_code==200:
        print response.text
        accessToken= re.findall(r"access_token\":\"([^\"]+)\"",response.text)[0]
        refreshToken= re.findall(r"refresh_token\":\"([^\"]+)\"",response.text)[0]
    # print error if bad request
    else: print "Access Token could not be created. Use verbose mode for more details"
    if verbose:
        print "Refresh Auth response:"
        print "Status: "+ str(response.status_code)
        print "Access Token: " +accessToken
        print "Refresh Token: " +refreshToken
        print "\n\n"
    ### DownScope Access Token ###
    # prepare downscope request (see:https://developer.box.com/reference#token-exchange)
    payload={
        'subject_token' : accessToken,
        'subject_token_type' : 'urn:ietf:params:oauth:token-type:access_token',
        'scope' : 'item_upload',
        'resource' : 'https://api.box.com/2.0/folders/'+str(folderID),
        'grant_type' : 'urn:ietf:params:oauth:grant-type:token-exchange'
    }
    # send post request
    response= requests.post("https://api.box.com/oauth2/token",payload)
    # parse result
    if response.status_code==200:
        accessToken= re.findall(r"access_token\":\"([^\"]+)\"",response.text)[0]
        expireTime= int(re.findall(r"expires_in\":(\d+)",response.text)[0])+ time.time()
    # print error for bad response
    else: print "Downscope Access Token cound not be created. Use verbose mode for more details"
    if verbose:
        print "DownScope Auth response"
        print "Status: "+ str(response.status_code)
        print "Acces Token:" + accessToken
        print "Expreation Time:" + str(expireTime)
        print "\n\n"


### Write all required ID's and Tokens to a configuration file ###
def writeCfg():
    global clientID, clientSecret, refreshToken, accessToken, expireTime
    with open("/Users/brenden/Desktop/git/Box_Upload/box.cfg", 'w') as cfg:
        cfg.write(clientID+"\n")
        cfg.write(clientSecret+"\n")
        cfg.write(refreshToken+"\n")
        cfg.write(accessToken+"\n")
        cfg.write(str(expireTime)+"\n")

### Read all required ID's and Tokens from configuration file ###
def readCfg():
    global clientID, clientSecret, refreshToken, accessToken, expireTime
    with open ("/Users/brenden/Desktop/git/Box_Upload/box.cfg", 'r') as cfg:
        clientID= cfg.readline().replace("\n","")
        clientSecret= cfg.readline().replace("\n","")
        refreshToken= cfg.readline().replace("\n","")
        accessToken= cfg.readline().replace("\n","")
        expireTime= float(cfg.readline().replace("\n",""))

# call main function
if __name__=="__main__":
    main()
