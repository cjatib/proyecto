import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import uuid
 
# MODIFY Registro 
#USER_POOL_ID = 'us-east-1_8VNNUGEcW'
#CLIENT_ID = '5h0v3fo9lj376auak93e2k8so3'
#CLIENT_SECRET = '3rmonpdf2sk0lnmpgpv12eaup93s6g4g406m90jh4nva6qp4k9r'

# DemoRegistro
USER_POOL_ID = 'us-east-1_bzGzM8xig'
CLIENT_ID = '4vnh0vah77mqibol4t5ds9e47t'
CLIENT_SECRET = 'd9s71eqhoh69eaqlpq5b6eo2thanev1p8hva4kcjqsa5tnbfdm4'

client = None

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
    
def initiate_auth(username, password):
    client = boto3.client('cognito-idp',region_name='us-east-1')
    print(client)
    secret_hash = get_secret_hash(username)
    print('desde Login_user')
    print(username)
    print(password)
    try:
        resp = client.initiate_auth(
                 #UserPoolId=USER_POOL_ID,
                 ClientId=CLIENT_ID,
                 #AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                 AuthFlow='USER_PASSWORD_AUTH',
                 #AuthFlow='ADMIN_NO_SRP_AUTH',
                 AuthParameters={
                     'USERNAME': username,
                     'SECRET_HASH': secret_hash,
                     'PASSWORD': password,
                  },
                ClientMetadata={
                  'username': username,
                  'password': password,
              })
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None


def lambda_handler(username,password):
    global client
    if client == None:
        client = boto3.client('cognito-idp')
    
    #print(event)
    #body = event
    #username = body['username']
    #password = body['password']
    
    resp, msg = initiate_auth(username, password)
    
    if msg != None:
        return {'message': msg, 
              "error": True, "success": False, "data": None}
    
    if resp.get("AuthenticationResult"):
        return {'message': "success", 
                "error": False, 
                "success": True, 
                "data": {
                "id_token": resp["AuthenticationResult"]["IdToken"],
                "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                "token_type": resp["AuthenticationResult"]["TokenType"]
                }}
    else: #this code block is relevant only when MFA is enabled
        return {"error": True, 
                "success": False, 
                "data": None, "message": None}
                
    