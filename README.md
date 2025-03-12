# 🖥️ Proyecto Django Snippets

Sistema web basado en Django con autenticación de usuarios, integración con Redis y Celery para tareas en segundo plano.

## 🚀 Tecnologías utilizadas

- **🐍 Django** – Framework web en Python.
- **🐘 MySQL** – Base de datos.
- **📝 Celery** – Procesamiento de tareas en segundo plano.
- **🔴 Redis** – Broker de mensajes para Celery.
- **💼 Control de versiones**: Git + GitHub.
- **🚀 Despliegue** - PythonAnywhere

---

## 📌 Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/miguelpuente/snippets_test/
cd django-snippets
```
2️⃣ Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```
4️⃣ Configurar variables de entorno

Renombrar .env.example a .env y editar con las credenciales necesarias:

```bash
mv .env.example .env
```

Modificar .env:
```bash
## Configuración Django
SECRET_KEY = django-insecure-dccp#!_))6bbals^!tlj=c(=@)c+2)v5$te6&likb_ud9zp9sd
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1, localhost

## Configuración Base de Datos MySql
DB_NAME = database_name
DB_USER = database_user
DB_PASSWORD = database_password
DB_HOST = database_host
DB_PORT = 3306

# Configuración Email (Ejemplo con Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=pass

## Configuración Redis
REDIS_URL=redis://localhost:6379/0
```
5️⃣ Migrar la base de datos
```bash
python manage.py migrate
```
6️⃣ Crear un superusuario
```bash
python manage.py createsuperuser
```
7️⃣ Iniciar el servidor web
```bash
python manage.py runserver
```

---

## ⚙️ Uso de Celery y Redis
Para ejecutar tareas en segundo plano:

▶️ Iniciar Redis (si está instalado localmente)
Linux/Mac:
```bash
redis-server
```
Windows: Usar Docker con:
```bash
docker run -d -p 6379:6379 redis
```

▶️ Iniciar el worker de Celery
```bash
celery -A django_snippets worker --loglevel=info
```

---

## 🌎 Despliegue en PythonAnywhere
El proyecto está desplegado en PythonAnywhere.

🔗 URL: https://miguepuente.pythonanywhere.com/
👤 Usuario: User
🔑 Contraseña: Demo2025

---

## 🤝 Contribuir
Si deseas mejorar este proyecto, haz un fork, envía un pull request o abre un issue.

📧 Contacto: itpuentemiguelangel@gmail.com