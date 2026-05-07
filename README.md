PROYECTO: SEGUIMIENTO ACADÉMICO
================================

Aplicación Django para gestión de proyectos académicos, comentarios y exportación de datos.

REQUISITOS PREVIOS
------------------
- Python 3.8 o superior instalado
- Git (opcional, para clonar el repositorio)

PASO A PASO PARA EJECUTAR LA APLICACIÓN
---------------------------------------

1. Clonar o descargar el repositorio
   git clone <URL-del-repositorio>
   cd seguimientoAcademico
   (Si no usas Git, simplemente descarga y extrae el código en una carpeta)

2. Crear y activar un entorno virtual
   Windows:
     python -m venv venv
     venv\Scripts\activate
   macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate

3. Instalar las dependencias
   pip install -r requirements.txt
   Si no tienes requirements.txt, instala al menos:
     pip install django django-crispy-forms crispy-bootstrap5

4. Aplicar las migraciones a la base de datos
   python manage.py migrate

5. Crear un usuario para acceder al sistema
   python manage.py createsuperuser
   Completa los datos:
     Usuario: (ej. admin)
     Correo: (ej. admin@example.com)
     Contraseña: (ej. admin123)
   GUARDA ESTAS CREDENCIALES PARA INICIAR SESIÓN.

6. En Admin aparece 2 opciones (Groups, Users) En Gruops crear Estudiante y Docente
7. En Users Crea 2 usuarios, te pedira username y contraseña y confirmacion de contraseña, una vez creada te saldra mas informacion
    Llena la informacion y en groups un usuario ponlo en Estudiante, y el otro usuario que crearas en Docente   

8. Ejecutar el servidor de desarrollo
   python manage.py runserver
   Verás: "Starting development server at http://127.0.0.1:8000/"

9. Acceder a la aplicación y loguearse
   Abre tu navegador y ve a:
     http://127.0.0.1:8000/login/
   Usa el usuario y contraseña que creaste en el paso 5.

10. Navegar por la aplicación
   Después del login serás redirigido a la lista de proyectos. Desde allí puedes:
     - Crear, editar, eliminar proyectos
     - Ver detalles y agregar comentarios
     - Exportar datos a CSV

ESTRUCTURA PRINCIPAL DEL PROYECTO
---------------------------------
- manage.py               - Punto de entrada del proyecto.
- settings.py             - Configuración (bases de datos, apps, directorios).
- urls.py                 - Rutas principales.
- proyectos_academicos/   - Aplicación con modelos, vistas y templates.

TECNOLOGÍAS UTILIZADAS
----------------------
- Django 6.0.5
- Bootstrap 5 (con crispy-forms)
- SQLite (base de datos por defecto)

CONTACTO / SOPORTE
------------------
Si tienes problemas, revisa la traza de errores en la terminal o en la consola del navegador. Asegúrate de haber ejecutado todas las migraciones y de que el servidor esté corriendo.
