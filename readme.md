Create virtual enviroment: python3 -m venv venv
Activate virtual enviroment: source venv/bin/activate
Install requirements: pip install -r requirements.txt

We have backend in python  on root and frontend with vuejs on src
backend run (path:/): 
- source venv/bin/activate
- python3 app.py  

This backend will work on http://fugaemfamilia.huna.pt/backoffice as a subdomain of huna.pt.
The endpoint will be:
- http://fugaemfamilia.huna.pt/backoffice/api/refresh_by_language
- http://fugaemfamilia.huna.pt/backoffice/api/options
- http://fugaemfamilia.huna.pt/backoffice/api/validate
- http://fugaemfamilia.huna.pt/backoffice/api/auth
- etc...

ATTENTION: need to update requirements.txt after installing new packages with following command:
pip freeze > requirements.txt

# Installation and Setup Instructions for hosting (CPaenel)


## Backend
Were we use python so to build  this for PRODUTION and use on hosting cpanel we need to follow the following steps:
- Create a subdomain on the host machine and point it to the root folder of the backend project. The subdomain should be named "backoffice" and the path should be "/". The subdomain should be created as a subdomain of huna.pt.
- Create a .htaccess file in the root folder of the backend project with the following content:

```
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ app.py [QSA,L]
```
- Create a venv folder in the root folder of the backend project with the following command:
```
python3 -m venv venv
```
- Activate the virtual environment with the following command:
```
source venv/bin/activate
```
- Install the required packages with the following command:
```
pip install -r requirements.txt
```
- Run the backend with the following command:
```
python3 app.py
```
- The backend should now be running on the subdomain "backoffice" of the host machine.

## Hosting
- The frontend should be accessible at the subdomain "backoffice" of the host machine.
- The backend should be accessible at the subdomain "backoffice" of the host machine.

# Installation and Setup Instructions for local machine

This project was bootstrapped with [Vue CLI], so it uses javascript and vuejs. To install and run the project, you need to have nodejs and npm installed on your local machine.

## Frontend
To install the project, you need to import the dist folder from the frontend project to the host machine. The dist folder is located in the src/frontend folder.
After importing the dist folder, you need to create a subdomain on the host machine and point it to the dist folder. The subdomain should be named "backoffice" and the path should be "/". The subdomain should be created as a subdomain of huna.pt.
After creating the subdomain, you need to create a .htaccess file in the dist folder with the following content:
```
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]


## FAQ

- **How do deal with error: python3: bad interpreter: No such file or directory**
    - rm -rf venv
    - python3 -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - python3 app.py

