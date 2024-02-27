from django.shortcuts import render
from backend.settings import *
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
# Create your views here.



@api_view(['POST', 'GET'])
def registerUser(request):
    action = 'registerUser'
    jsons = json.loads(request.body)
    action = jsons.get('action', 'nokey')
    email = jsons.get('email', 'nokey')
    lname = jsons.get('lname', 'nokey')
    fname = jsons.get('fname', 'nokey')
    passw = jsons.get('passw', 'nokey')
    
    con = connect()
    cursor = con.cursor()

    # Check if email already exists and is enabled
    cursor.execute(f"SELECT COUNT(*) FROM t_users WHERE email = '{email}' AND enabled = 1")
    count = cursor.fetchone()[0]
    print(count)
    if count==1:
        resp = sendResponse(401, f'{email} emailtei hereglegch burtgeltei bn', action)
        return HttpResponse(resp)

    # Insert new user
    try:
        cursor.execute("INSERT INTO t_users (lname, fname, passw, enabled, email) VALUES (%s, %s, %s, %s, %s)",
                       (lname, fname, passw, 1, email))
        con.commit()  # Commit the transaction
        resp = sendResponse(200, f'{email} хэрэглэгчийг амжилттай бүртгэлээ', action)
        return HttpResponse(resp)
    except Exception as e:
        # Handle database errors
        error_message = "Database error: " + str(e)
        resp = sendResponse(500, error_message, action)
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
            resp = sendResponse(400, f"{mname} kino ali hediin burtgegdsen bn", action)
        else:
            # Movie doesn't exist, insert it into the database
            cursor.execute(f"""INSERT INTO t_movie(mname, mauth, mtorol) 
                                VALUES('{mname}', '{mauth}', '{mtorol}')""")
            con.commit()
            resp = sendResponse(200, f"{mname} kino amjilttai burtgegdlee", action)
        
        return HttpResponse(resp)
    except Exception as e:
        # Handle database errors
        error_message = "Database error: " + str(e)
        resp = sendResponse(500, error_message, action)
        return HttpResponse(resp)

