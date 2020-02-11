from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request, *args, **kwargs):
        if not request.session.get('login', False):
            return render(request, 'main.html')
        else:
            return render(request, 'chat/index.html', {'Name': request.session.get('user_name')})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)) , 'Name':request.session.get('user_name')
    })