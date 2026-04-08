# � PolyStation2

> PolyStation2 es un sistema Django para e-commerce con roles distribuidor/comprador, autenticación y APIs REST.

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/?hl=es-419)

---

## 📋 Tabla de contenidos

- [Descripción](#-descripción)
- [Requisitos](#-requisitos)
- [Instalación paso a paso](#-instalación-paso-a-paso)
- [Stack tecnológico](#-stack-tecnológico)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Documentación API](#-documentación-api)
- [Cuentas de prueba](#-cuentas-de-prueba)
- [Autores](#-autores)
- [Documentación Link](#link-del-drive-documentación-del-proyecto)

---

## 📦 Descripción
PolyStation2 es una plataforma de comercio en Django con dos roles:
- **comprador**: navega productos, hace pedidos, consulta su perfil.
- **distribuidor**: administra stock, pedidos y su panel.

Incluye autenticación JWT/Firebase, permisos por rol y APIs REST.

---

## ✅ Requisitos

- Python 3.11+ (recomendado)
- pip
- virtualenv
- Windows/Mac/Linux
- Extension REST CLIENT (Para hacer pruebas de HTTP)

---

## 🚀 Instalación paso a paso

```powershell

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py runserver
```

Prueba con el test.http.

---

## 🧱 Stack tecnológico

- Django
- Django REST Framework
- Firebase Admin (autenticación/configuración)
- HTTP

---

## 🗂️ Estructura del proyecto

```
PolyStation2/
├── principalstation/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── firebase_config.py
│   └── serviceAccountKey.json
├── gamestation/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views_auth.py
│   ├── views_comprador.py
│   ├── views_distribuidor.py
│   ├── views_perfil.py
│   └── urls.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔎 Documentación API 

---

## 🔐 Nombres y cuentas de Github

  - Johan Sebastian Castro Gonzalez: `zsatorii`
  - Pablo Mozuca Chaparro: `PabloMSL`
  - Santiago Beltran Pedraza: `Santiago-Beltran1`

---

## Link del drive documentación del proyecto 

  - Link del drive: [Link drive]

---