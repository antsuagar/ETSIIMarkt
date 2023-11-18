# ETSIIMarkt

## **INSTRUCCIONES DE INSTALACIÓN**
1. Instalar python 3.11(se puede hacer desde la Microsoft Store, es muy fácil y cómodo). Comprobarlo en un cms con el comando python --version.
2. Abrir Visual Studio Code
3. Importar el repositorio(Ctrl+Shift+P, escribe git clone y pega la dirección del repositorio: https://github.com/antsuagar/ETSIIMarkt/)
4. Abrir una terminal en Visual Studio Code(Terminal>New terminal)
5. cd ..
6. python -m venv env
7. Set-ExecutionPolicy Unrestricted -Scope Process
8. env\Scripts\activate
9. cd ETSIIMARKT
10. pip install -r requirements.txt
Una vez acabe ya está todo instalado. Para empezad a trabajar cerrad la ventana de Visual Studio Code y seguid las siguientes instrucciones.

## **INSTRUCCIONES DE USO**
Cuando Visual Studio Code se abra estaréis en la carpeta base del repositorio. Para empezar a trabajar haced:
1. cd ..
2. Set-ExecutionPolicy Unrestricted -Scope Process
3. env\Scripts\activate
4. cd ETSIIMARKT
5. cd EtsiiMarktProject
Una vez ahí podeis hacer varias cosas:
- Lanzar la aplicación: python manage.py runserver. Paradla con Ctrl+C.
- Crear una nueva aplicación de Django: django-admin startapp nombre_app