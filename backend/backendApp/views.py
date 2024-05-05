from django.shortcuts import render
from backend.settings import *
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
from datetime import date
import jwt
from datetime import datetime, timedelta
import random
import hashlib
import io
import pytesseract
from PIL import Image
import base64
from io import BytesIO
@api_view(['POST', 'GET'])
def registerUser(request):
    action = 'registerUser'
    jsons = json.loads(request.body)
    action = jsons.get('action', 'nokey')
    email = jsons.get('email', 'nokey')
    lname = jsons.get('lname', None)  # Allow None for empty values
    fname = jsons.get('fname', None)  # Allow None for empty values
    passw = jsons.get('passw', 'nokey')
    # Check if first name and last name are provided    
    if not fname or not lname:
        data = [{"message":"ta buh talbariig boglono uu"}]
        resp = sendResponse(request,400, "Та бүх талбарыг бөглөнө үү!", action)
        return HttpResponse(resp)

    con = connect()
    cursor = con.cursor()

    # Check if email already exists and is enabled
    cursor.execute(f"SELECT COUNT(*) FROM t_users WHERE email = '{email}' AND enabled = 1")
    count = cursor.fetchone()[0]
    # print(count)
    if count == 1:
        data = [{"email":email}]
        resp = sendResponse(request,1000,data,action)
        return HttpResponse(resp)
    verification_code = generate_verification_code()  # Implement your own function to generate a verification code

    # Send verification code via email
    send_verification_email(email, verification_code,lname,fname)

    # Insert new user
    try:
        cursor.execute("INSERT INTO t_users (lname, fname, passw, enabled, email) VALUES (%s, %s, %s, %s, %s)",
                       (lname, fname, passw, 1, email))
        con.commit()  # Commit the transaction
        data = [{'email':email, 'firstname':fname, 'lastname': lname}]
        resp = sendResponse(request,200, data, action)
        return HttpResponse(resp)
    except Exception as e:
        # Handle database errors
        error_message = "Database error: " + str(e)
        resp = sendResponse(request,500, error_message, action)
        return HttpResponse(resp)
    
@api_view(['POST', 'GET'])
def loginUser(request):
    action = 'loginUser'
    jsons = json.loads(request.body)
    action = jsons.get('action', 'nokey')
    email = jsons.get('email', 'nokey')
    passw1 = jsons.get('passw', 'nokey')
    passw = hashlib.md5(hashlib.md5(passw1.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
    print(passw+"==AAA=="+passw1)
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(f"SELECT passw FROM t_users WHERE email = '{email}'")
        dbpassw = cursor.fetchall()[0][0]
        
        if dbpassw != passw:
            data=[{"password":passw}]
            resp = sendResponse(request,1004,data, action)
            return HttpResponse(resp)

        cursor.execute(f"SELECT uid FROM t_users WHERE email = '{email}'")
 
        user_id = cursor.fetchall()[0][0]
        print(user_id)
        if user_id == 0:
            data = [{"email":email}]
            resp = sendResponse(request,1000,data, action)
            return HttpResponse(resp)
        token = generate_token(user_id)
       
        cursor.execute("INSERT INTO t_token (uid, token) VALUES (%s, %s)",
                       (user_id,token))
        con.commit()
        data = [{'uid':user_id,'email':email,"token":token}]

        resp = sendResponse(request,200, data, action)
        return HttpResponse(resp)
        
    except Exception as e:
        # Handle database errors
        data = [{"Database error": str(e)}]
        resp = sendResponse(request,500, data, action)
        return HttpResponse(resp)

    
@api_view(['POST', 'GET'])
def addMovie(request):
    action = 'addMovie'
    jsons = json.loads(request.body)
    mname = jsons.get('mname','nokey')
    mauth = jsons.get('mtorol','nokey')
    mtorol = jsons.get('mauth','nokey')
   
    con = connect()
    cursor = con.cursor()

    try:
        # Check if the movie already exists in the database
        cursor.execute(f"SELECT * FROM t_movie WHERE mname = '{mname}' AND mauth = '{mauth}' AND mtorol = '{mtorol}'")
        existing_movie = cursor.fetchone()
        if existing_movie:
            # Movie already exists, send a response indicating that
            resp = sendResponse(request,400, f"{mname} kino ali hediin burtgegdsen bn", action)
        else:
            # Movie doesn't exist, insert it into the database
            cursor.execute(f"""INSERT INTO t_movie(mname, mauth, mtorol) 
                                VALUES('{mname}', '{mauth}', '{mtorol}')""")
            con.commit()
            resp = sendResponse(request,200, f"{mname} kino amjilttai burtgegdlee", action)
        
        return HttpResponse(resp)
    except Exception as e:  
        # Handle database errors
        error_message = "Database error: " + str(e)
        resp = sendResponse(request,500, error_message, action)
        return HttpResponse(resp)

@api_view(['POST', 'GET'])
def bookadd(request):
    action = 'bookadd'
    jsons = json.loads(request.body)
    bname = jsons.get('bname','nokey')
    author = jsons.get('author','nokey')
    btype = jsons.get('btype','nokey')
   
    con = connect()
    cursor = con.cursor()

    try: 
        cursor.execute(f"SELECT * FROM t_book WHERE bname = '{bname}' AND author = '{author}' AND btype = '{btype}'")
        existing_bookadd = cursor.fetchone()
        if existing_bookadd:
            resp = sendResponse(request,400, f"{bname} ном бүртгэгдсэн байна", action)
        else:
            cursor.execute(f"""INSERT INTO t_book(bname, author, btype) VALUES('{bname}', '{author}', '{btype}')""")
            con.commit()
            resp= sendResponse(request,200, f"{bname} номыг бүртгэлээ", action)

        return HttpResponse(resp)
    except Exception as e:
        # Handle database errors
        error_message = "Database error: " + str(e)
        resp = sendResponse(request,500, error_message, action)
        return HttpResponse(resp)
    

def gettime(request):
        today = date.today()
        return HttpResponse(today)
def userregister(request):
        jsons = json.loads(request.body)
        return HttpResponse(jsons['action'])

def checkService(request):
    jsons = json.loads(request.body)
    if jsons['action']=='gettime':
        result (jsons)
    elif jsons['action']=='register': 
        result=userregister(request)
    else:
        result ('action buruu bnaa')
    return HttpResponse(result)

@api_view(['POST', 'GET'])
def b64Text(request):
    action = 'base64ToText'
    jsons = json.loads(request.body)
    action = jsons.get('action', 'nokey')
    b64 = jsons.get('base64', 'nokey')
    image_data = base64.b64decode(b64)
    image = Image.open(io.BytesIO(image_data))
    extracted_text = pytesseract.image_to_string(image)
    data = [{"text":extracted_text}]
    print(data)
    resp = sendResponse(request,200, data, action)
    return HttpResponse(resp)

  



def generate_token(count):
    try:
        # Define payload with user identifier (count value) and expiration time
        payload = {
            'user_id': count,
            'exp': datetime.now() + timedelta(days=1)  # Token expiration time (1 day)
        }

        # Encode payload and return token
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token  # No need to decode here
    except Exception as e:
        # Handle token generation errors
        error_message = "Token generation error: " + str(e)
        print(error_message)
        return None
    


def generate_verification_code():
    # Generate a random 6-digit verification code
    return ''.join(random.choices('0123456789', k=6))    