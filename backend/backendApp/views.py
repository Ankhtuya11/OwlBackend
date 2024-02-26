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
                       (lname, fname, passw, 0, email))
        con.commit()  # Commit the transaction
        resp = sendResponse(200, f'{email} хэрэглэгчийг амжилттай бүртгэлээ', action)
        return HttpResponse(resp)
    except Exception as e:
        # Handle database errors
        error_message = "Database error: " + str(e)
        resp = sendResponse(500, error_message, action)
        return HttpResponse(resp)
    

