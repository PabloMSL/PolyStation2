from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore, auth
from principalstation.firebase_config import initialize_firebase
from functools import wraps
import requests
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


db = initialize_firebase()


def login_required_firebase(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        uid = request.session.get('uid')
        if not uid:
            messages.error(request, "Debes iniciar sesión")
            return redirect('login_comprador')
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt  # no rebote el error 403 de CSRF
def registro_comprador(request):
    if request.method == 'POST':
        try:
            # 1. Cargar los datos del JSON
            data = json.loads(request.body)
            
            # 2. Obtener los campos (usa los mismos nombres que mandas en el JSON)
            nombre = data.get('username') # En tu JSON mandas "username", no "nombre"
            email = data.get('email')
            password = data.get('password')

            # 3. Validación básica
            if not email or not password:
                return JsonResponse({"error": "Faltan datos obligatorios"}, status=400)

            # 4. Crear usuario en Firebase
            user = auth.create_user(
                email=email,
                password=password
            )

            # 5. Guardar en Firestore
            db.collection('usuarios').document(user.uid).set({
                'nombre': nombre,
                'email': email,
                'uid': user.uid,
                'rol': 'comprador',
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            return JsonResponse({"mensaje": "Usuario registrado", "uid": user.uid}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def login_comprador(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            api_key = os.getenv('FIREBASE_WEB_API_KEY')

            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            response = requests.post(url, json=payload)
            fb_data = response.json()

            if response.status_code == 200:
                # En una API, solemos devolver el token para que el cliente lo guarde
                # Pero si usas sesiones de Django, las mantenemos:
                request.session['uid'] = fb_data['localId']
                request.session['email'] = fb_data['email']
                request.session['rol'] = 'comprador'

                return JsonResponse({
                    "mensaje": "Login exitoso",
                    "token": fb_data.get('idToken'),
                    "uid": fb_data['localId']
                }, status=200)
            else:
                return JsonResponse({"error": "Credenciales inválidas"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)