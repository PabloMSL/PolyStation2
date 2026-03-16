from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from firebase_admin import firestore, auth
from principalstation.firebase_config import initialize_firebase
from functools import wraps
import requests
import os
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


db = initialize_firebase()


def login_required_firebase(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        uid = request.session.get('uid')
        if not uid:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect({"error": "No autorizado. Debes iniciar sesión."}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
def registro_distribuidor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            nombre = data.get('nombre')
            empresa = data.get('empresa')
            telefono = data.get('telefono')

            user = auth.create_user(email=email, password=password)

            db.collection('distribuidores').document(user.uid).set({
                'nombre': nombre,
                'empresa': empresa,
                'telefono': telefono,
                'email': email,
                'uid': user.uid,
                'rol': 'distribuidor',
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            return JsonResponse({"mensaje": "Distribuidor registrado correctamente", "uid": user.uid}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def login_distribuidor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            api_key = os.getenv('FIREBASE_WEB_API_KEY')

            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            payload = {"email": email, "password": password, "returnSecureToken": True}

            response = requests.post(url, json=payload)
            fb_data = response.json()

            if response.status_code == 200:
                request.session['uid'] = fb_data['localId']
                request.session['email'] = fb_data['email']
                request.session['rol'] = 'distribuidor'
                return JsonResponse({"mensaje": "Login exitoso", "uid": fb_data['localId']}, status=200)
            else:
                return JsonResponse({"error": "Credenciales incorrectas"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)