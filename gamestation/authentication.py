from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from principalstation.firebase_config import initialize_firebase

db = initialize_firebase()


class FirebaseUser:
    def __init__(self, uid, rol, email):
        self.uid = uid
        self.rol = rol
        self.email = email
        self.is_authenticated = True
        self.is_active = True

    def __str__(self):
        return self.email


class FirebaseAuthentication(BaseAuthentication):
    """
    Lee el token JWT del encabezado Authorization,
    lo valida con Firebase y extrae el usuario con su rol real desde Firestore.
    Compatible con:
    - perfiles
    - usuarios
    - distribuidores
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION') or request.headers.get('Authorization')

        if not auth_header:
            return None

        partes = auth_header.split()

        if len(partes) != 2 or partes[0].lower() != 'bearer':
            return None

        token = partes[1]

        try:
            decoded_token = auth.verify_id_token(token)

            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            rol = decoded_token.get('rol')  # si viene en custom claims

            if not uid:
                raise AuthenticationFailed("No se encontró el UID en el token")

            # =========================================================
            # 1) Primero buscar en perfiles (REST API moderna)
            # =========================================================
            if not rol:
                perfil_doc = db.collection('perfiles').document(uid).get()
                if perfil_doc.exists:
                    rol = perfil_doc.to_dict().get('rol')

            # =========================================================
            # 2) Luego buscar en usuarios (compradores)
            # =========================================================
            if not rol:
                usuario_doc = db.collection('usuarios').document(uid).get()
                if usuario_doc.exists:
                    rol = usuario_doc.to_dict().get('rol')

            # =========================================================
            # 3) Luego buscar en distribuidores
            # =========================================================
            if not rol:
                distribuidor_doc = db.collection('distribuidores').document(uid).get()
                if distribuidor_doc.exists:
                    rol = distribuidor_doc.to_dict().get('rol')

            # =========================================================
            # 4) Si no aparece en ninguna colección
            # =========================================================
            if not rol:
                raise AuthenticationFailed("No se encontró el rol del usuario en Firestore")

            return (FirebaseUser(uid, rol, email), decoded_token)

        except Exception as e:
            raise AuthenticationFailed(f"Token no válido o expirado: {str(e)}")