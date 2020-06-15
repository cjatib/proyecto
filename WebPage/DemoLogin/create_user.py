import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import uuid
 
# MODIFY / Cognito Registro
#USER_POOL_ID = 'us-east-1_8VNNUGEcW'
#CLIENT_ID = '5h0v3fo9lj376auak93e2k8so3'
#CLIENT_SECRET = '3rmonpdf2sk0lnmpgpv12eaup93s6g4g406m90jh4nva6qp4k9r'

# MODIFY / Cognito DemoRegistro
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

def lambda_handler(username,password,email,name,family_name):
    
    
    global client
    if client == None:
        client = boto3.client('cognito-idp',region_name='us-east-1')
        print(client)

    #print(event)
    #body = event
    #username = body['username']
    #password = body['password']
    #email = body['email']
    #name = body['name']
    #family_name = body['family_name']

    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'name',
                    'Value': name
                },
                {
                    'Name': 'family_name',
                    'Value': family_name
                },
            ],
            ValidationData=[
                {
                    'Name': 'email',
                    'Value': email
                },
        ])
            
        print(resp)
    except client.exceptions.UsernameExistsException as e:
        return {"error": True, 
               "success": False, 
               "message": "Este usuario ya esta registrado.", 
               "data": None} 
    except client.exceptions.InvalidPasswordException as e:
        return {"error": True, 
               "success": False, 
               "message": "La contraseña debe tener mayúsculas, minúsculas, un carácter especial y números.", 
               "data": None}
    except Exception as e:
        return {"error": True, 
                "success": False, 
                "message": str(e), 
               "data": None}
    return {"error": False, 
            "success": True, 
            "message": "Registro Exitoso. Revisa tu Email para validar tu correo.", 
            "data": None}    