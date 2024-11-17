# app.py
version='1.0.4'

from flask import Flask, jsonify
from flask_cors import CORS
from models.reservation import Reservation  # Adjust the import path based on your project structure
import pandas as pd
from flask import request
from services.olx_api import authenticate_olx, check_olx_status
import requests
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://fugaemfamilia-frontoffice.huna.pt", "http://localhost:5000", "http://192.168.152.2:8080"
, "http://192.168.1.184:8080"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')
TTL_ACCESS_TOKEN = 1 # in days

# Global variable declaration
reservations = []

@app.route('/api/options')
def get_options():
    options = [ (reservation.id,reservation.nome) for reservation in reservations]
    return jsonify(options)

def import_all_reservations( language = 'pt'):
    data = read_from_google_spreadsheets(language)  
    global reservations
    if language == 'pt':
        try:
            for index, row in data.iterrows():
                reservation = Reservation(
                    id=row['id'],
                    nome=row['O seu nome'] if pd.notna(row['O seu nome']) else "",
                    phone=row['Contacto telefonico'] if pd.notna(row['Contacto telefonico']) else "",
                    email=row['Contacto Email'] if pd.notna(row['Contacto Email']) else "",
                    localidade=row['A sua localidade'] if pd.notna(row['A sua localidade']) else "",
                    metodo_de_contacto=row['Metodo de contacto preferido?'] if pd.notna(row['Metodo de contacto preferido?']) else "",
                    data_de_partida = pd.to_datetime(row['Data de Partida']) if pd.notna(row['Data de Partida']) else None,
                    hora_da_partida=row['Hora da Partida'] if pd.notna(row['Hora da Partida']) else "",
                    data_de_chegada = pd.to_datetime(row['Data de Chegada']) if pd.notna(row['Data de Chegada']) else None,
                    hora_da_chegada=row['Hora da Chegada'] if pd.notna(row['Hora da Chegada']) else "",
                    localdepartida=row['Local de partida'] if pd.notna(row['Local de partida']) else "",
                    localdechegada=row['Local de chegada'] if pd.notna(row['Local de chegada']) else "",
                    adultos=row['Nº de passageiros [Adultos]'] if pd.notna(row['Nº de passageiros [Adultos]']) else "",
                    criancas=row['Nº de passageiros [Crianças]'] if pd.notna(row['Nº de passageiros [Crianças]']) else "",
                    animais=row['Nº de passageiros [Cães ou gatos]'] if pd.notna(row['Nº de passageiros [Cães ou gatos]']) else "",
                    destino=row['Destino'] if pd.notna(row['Destino']) else "",
                    tipo_de_viagem=row['Tipos de férias'] if pd.notna(row['Tipos de férias']) else "",
                    Pernoitar=row['Pernoitar'] if pd.notna(row['Pernoitar']) else "",
                    tem_experiencia=row['Tem experiência em usar e conduzir uma autocaravana?'] if pd.notna(row['Tem experiência em usar e conduzir uma autocaravana?']) else "",
                    extras={k.split('[')[-1].strip(']'): row[k] if pd.notna(row[k]) else "" for k in row.keys() if k.startswith('Opcionais')},
                    vem_de_onde=row['Como soube da nossa autocaravana?'] if pd.notna(row['Como soube da nossa autocaravana?']) else "",
                    questions_and_comments=row['Perguntas ou comentários?'] if pd.notna(row['Perguntas ou comentários?']) else ""
                )
                reservations.append(reservation)
            print(f"Successfully imported {len(reservations)} reservations")
            return reservations
        except Exception as e:
            print(f"Error 103: {e}")
            return []
    elif language == 'en':
        try:
            for index, row in data.iterrows():
                reservation = Reservation(
                    nome=row['O seu nome'] if pd.notna(row['O seu nome']) else "",
                    phone=row['Contacto telefonico'] if pd.notna(row['Contacto telefonico']) else "",
                    email=row['Contacto Email'] if pd.notna(row['Contacto Email']) else "",
                    # contactos=row['Contactos pessoais'] if pd.notna(row['Contactos pessoais']) else "",
                    localidade=row['A sua localidade'] if pd.notna(row['A sua localidade']) else "",
                    metodo_de_contacto=row['Metodo de contacto preferido?'] if pd.notna(row['Metodo de contacto preferido?']) else "",

                    data_de_partida = pd.to_datetime(row['Data de Partida']) if pd.notna(row['Data de Partida']) else None,
                    hora_da_partida=row['Hora da Partida'] if pd.notna(row['Hora da Partida']) else "",
                    data_de_chegada = pd.to_datetime(row['Data de Chegada']) if pd.notna(row['Data de Chegada']) else None,
                    hora_da_chegada=row['Hora da Chegada'] if pd.notna(row['Hora da Chegada']) else "",
                    localdepartida=row['Local de partida'] if pd.notna(row['Local de partida']) else "",
                    localdechegada=row['Local de chegada'] if pd.notna(row['Local de chegada']) else "",

                    adultos=row['Nº de passageiros [Adultos]'] if pd.notna(row['Nº de passageiros [Adultos]']) else "",
                    criancas=row['Nº de passageiros [Crianças]'] if pd.notna(row['Nº de passageiros [Crianças]']) else "",
                    animais=row['Nº de passageiros [Cães ou gatos]'] if pd.notna(row['Nº de passageiros [Cães ou gatos]']) else "",

                    destino=row['Destino'] if pd.notna(row['Destino']) else "",
                    tipo_de_viagem=row['Tipos de férias'] if pd.notna(row['Tipos de férias']) else "",
                    Pernoitar=row['Pernoitar'] if pd.notna(row['Pernoitar']) else "",
                    tem_experiencia=row['Tem experiência em usar e conduzir uma autocaravana?'] if pd.notna(row['Tem experiência em usar e conduzir uma autocaravana?']) else "",
                    extras={k.split('[')[-1].strip(']'): row[k] if pd.notna(row[k]) else "" for k in row.keys() if k.startswith('Opcionais')},
                    vem_de_onde=row['Como soube da nossa autocaravana?'] if pd.notna(row['Como soube da nossa autocaravana?']) else "",
                    questions_and_comments=row['Perguntas ou comentários?'] if pd.notna(row['Perguntas ou comentários?']) else ""
                )
                reservations.append(reservation)
            print(f"Successfully imported {len(reservations)} reservations")
            return reservations
        except Exception as e:
            print(f"Error 104: {e}")
            return []
    else:
        print("Error 105: Language not found")
        return []   

def read_from_google_spreadsheets(language = 'pt'):
    if language == 'pt':
        url = 'https://docs.google.com/spreadsheets/d/1cVQKa3lvpoQPmtRyRcJxB8CAjfkSEuSKOi8hLWH6Ekk/export?format=csv'
    elif language == 'en':
        url = 'https://docs.google.com/spreadsheets/d/1IBEKqCZdHL154-SQcV-QeHwKL7a7Z01h-45falR8uHo/export?format=csv'
    else:
        print("Error 101: Language not found")
        exit(1)
    data = pd.read_csv(url)
    # // id of data
    # add id for each row
    data['id'] = data.index
    print("data: ", data)
    if data.empty:
        print("No data found")
        exit(1)
    else:
        print("Data loaded successfully: ", data.shape)
        return data

@app.route('/ping')
def ping():
    return jsonify({"message": "Pong"})

@app.route('/version')
def get_version():
    return jsonify({"version": version})

@app.route('/api/reservation')
def get_reservation():
    name = request.args.get('name')
    id = request.args.get('id')
    if name and id:
        reservation = next((reservation for reservation in reservations if reservation.nome == name and reservation.id == int(id)), None)
        if reservation:
            return jsonify([reservation.__dict__])
    # return an error message if the name is not found
    return jsonify({"error": "Name not found"})

@app.route('/api/all_reservations')
def get_all_reservations():
    return jsonify([reservation.__dict__ for reservation in reservations])

@app.route('/api/refresh' , methods=['POST'])
def refresh_data():
    global reservations
    if reservations is not None:
        del reservations[:]
    reservations = import_all_reservations()
    return jsonify({"message": "Data refreshed successfully"})

# this route api/refresh_by_language will refresh the data using the language parameter cames from the request
@app.route('/api/refresh_by_language' , methods=['POST'])
def refresh_data_by_language():
    language = request.json.get('language')
    if language:
        global reservations
        if reservations is not None:
            del reservations[:]
        reservations = import_all_reservations(language)
        return jsonify({"message": f"Data refreshed successfully using language: {language}"})
    return jsonify({"error": "Language parameter not found"})

@app.route('/check-olx-status', methods=['GET'])
def check_status():
    try:
        access_token = authenticate_olx()
        status_code = check_olx_status(access_token)
        if status_code == 200:
            return jsonify({'message': 'Request was successful with status 200'}), 200
        else:
            return jsonify({'message': f'Request failed with status: {status_code}'}), status_code
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.get_json()
    secret_key = data.get('secretKey')
    if secret_key == AUTH_PASSWORD:
        token = jwt.encode({
            'authenticated': True,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=TTL_ACCESS_TOKEN)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'authenticated': True, 'token': token})
    else:
        return jsonify({'authenticated': False}), 401

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    token = data.get('token')
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'valid': True})
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'error': 'Invalid token'}), 401

if __name__ == '__main__':
    # print
    print("Starting the server")
    reservations = import_all_reservations()
    for reservation in reservations:
        print(reservation.__dict__)
        print(reservation.nome)
    app.run(debug=True)