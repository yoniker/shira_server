from flask import Flask
from flask import jsonify, request, send_from_directory, redirect
from postgres_client import PostTBD
import ast
import flask
from sql_consts import SQL_CONSTS
from error_consts import ERROR_CONSTS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os
import requests
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

EXAMINATIONS_INTERVALS = {'ultrasound_1': 6, 'sisi_shelia' : 10, 'shkifut_orpit' : 11, 'skirat_marchot_mukdemet' : 14, 'helbon_ubari' : 16,
                          'dikur_mi_shafir' : 16, 'skirat_marchot_meucheret' : 19, 'hamasat_sugar' : 24, 'ultrasound_2' : 30,
                          'tarbit_gbs' : 35, 'nitur_ubari' : 38}  # In weeks

VACCINES_INTERVALS = {'tzhevet_b_mana_1' : 0, 'tzhevet_b_mana_2' : 1, 'tzhevet_b_mana_3' : 6, 'paletzet_mana_1' : 2, 'paletzet_mana_2' : 4, 'paletzet_mana_3' : 6, 'paletzet_mana_4' : 12,
                      'polio_1' : 6, 'polio_2' : 18, 'hemofilos_mana_1' : 2, 'hemofilos_mana_2' : 4, 'hemofilos_mana_3' : 6, 'hemofilos_mana_4' : 12, 'pnoimokok_nama_1' : 2, 'pnoimokok_nama_2' : 4, 'pnoimokok_nama_3' : 12,
                      'negif_rota_mana_1' : 2, 'negif_rota_mana_2' : 4, 'negif_rota_mana_3' : 6, 'hatzevet_hazeret_ademet_hababuot' : 12,
                      'tzhevet_a_mana_1' : 18, 'tzhevet_a_mana_2' : 24} #in month


USERS_DATA_DIR = '/media/yoni/PapushDisk11/shira_data'

WOMEN_EMAIL_REMINDER_DAYS_BEFORE_EXAMINATION = 3
EMAIL_REMINDER_DAYS_BEFORE_VACCINE = 3

app = Flask(__name__)
postgres_client = PostTBD()  # TODO move to app.config


def send_email(email,content):
    if email is None or len(email)==0:
        return #Not a valid email address TODO use regex that it is a valid email
    print(f'Will send {content} to {email}')
    requests.post('http://shira.voilaserver.com/shira/send_email',
                  json={"sender":"finalprojecttest22@gmail.com","to_address":email,"subject":"Notification","text_message":content})

def notify_examination(email, woman_name, examination_name):
    send_email(email=email,content=(
        
        f"Hi {woman_name}!"
        f"This is a reminder that in {WOMEN_EMAIL_REMINDER_DAYS_BEFORE_EXAMINATION} day, "
        f" you have to take the examination {examination_name}!"
        f"Truly yours,"
        f"Dor."
        
    ))


def notify_vaccine(email, woman_name,child_name, vaccine_name):
    send_email(email=email, content=(
        
        f"Hi {woman_name}!"
        f"This is a reminder that in {WOMEN_EMAIL_REMINDER_DAYS_BEFORE_EXAMINATION} day, "
        f" you have to take your child {child_name} to take the vaccine {vaccine_name}!"
        f"Truly yours,"
        f"Dor."
    
    ))

def send_notifications():
    #Iterate over women examinations and send a notification if needed
    for examination_name,weeks_into_pregnancy in EXAMINATIONS_INTERVALS.items():
        women_to_notify = postgres_client.get_women_by_days_from_last_period(weeks_into_pregnancy*7-WOMEN_EMAIL_REMINDER_DAYS_BEFORE_EXAMINATION)
        for woman in women_to_notify:
            if not woman.get(examination_name,False): #If the woman didn't take the examination yet
                notify_examination(email=woman.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value, ''),
                                   woman_name=woman.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value,'Dear'),
                                   examination_name=examination_name)
                
    for vaccine_name,age_months in VACCINES_INTERVALS:
        relevant_children_details = postgres_client.get_children_by_days_from_birthday(days_from_birthday=age_months*30-EMAIL_REMINDER_DAYS_BEFORE_VACCINE)
        for child in relevant_children_details:
            if not child.get(vaccine_name,False):
                notify_vaccine(email = child.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value,''),
                               woman_name=child.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value),
                               child_name=child.get(SQL_CONSTS.CHILDREN_DETAILS.CHILD_NAME.value,''),
                               vaccine_name=vaccine_name)

send_notifications()
scheduler = BackgroundScheduler()
scheduler.add_job(func=send_notifications, trigger="interval", seconds=60*60*24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
'''
for security, we are going to use JWT so that the server won't have to remember a temporary session token
The client has to add the JWT token to each request (via the standrad header "Authorization")
'''

app.config["JWT_SECRET_KEY"] = "shira's huge server secret"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
jwt = JWTManager(app)

# create_access_token() function is used to actually generate the JWT.
@app.route("/login/", methods=["POST"])
def login():
    username = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value, None)
    password = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value, None)
    actual_user_details = postgres_client.get_woman_details(woman_id=username)  # In other apps user_id could be different than username so this might have been different
    if actual_user_details is None or actual_user_details[SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value] != password:
        return jsonify({"status": "Bad username or password"}), 401

    access_token = create_access_token(identity=username) #Create the JWT token so that the user can access routes
    return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.SUCCESSFUL_LOGIN,'access_token':access_token})


@app.route("/register/", methods=["POST"])
def register():
    username = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value, None)
    password = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value, None)
    full_name = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value, None)
    actual_user_details = postgres_client.get_woman_details(woman_id=username)  # In other apps user_id could be different than username so this might have been different
    if actual_user_details is not None:
        return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS: ERROR_CONSTS.STATUS_ERROR.USER_ALREADY_EXIST}), 401

    postgres_client.add_woman(woman_details = request.json)
    return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.SUCCESSFUL_LOGIN})


@app.route('/hello', methods=['GET'])
def say_hello():
    return jsonify({'response': 'hello'})


@app.route('/get_woman_details/<woman_id>')
@jwt_required()
def get_woman_id(woman_id):
    # TODO security eg make sure that woman_id is accessing it via a session token/JWT
    user_the_jwt_belongs_to = get_jwt_identity()
    if user_the_jwt_belongs_to != woman_id:
        return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.ANOTHER_USER_LOGGED_IN}),400
    data = postgres_client.get_woman_details(woman_id=woman_id)
    if data is None:
        return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.MISSING_DETAILS}), 400
    data = dict(data)
    return jsonify(data)


@app.route('/get_child_details/<child_id>')
@jwt_required()
def get_child_id(child_id):
    data = postgres_client.get_child_details(child_id=child_id)
    if data is None:
        return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.MISSING_DETAILS}), 400
    data = dict(data)
    user_the_jwt_belongs_to = get_jwt_identity()
    if user_the_jwt_belongs_to != data[SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value]:
        return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS: ERROR_CONSTS.STATUS_ERROR.ANOTHER_USER_LOGGED_IN}), 400
    return jsonify(data)




@app.route('/save_child_details/', methods=['POST'])
@jwt_required()
def save_child_details():
    # flask.request.files.get('file', '')

    dict_str = request.data.decode("UTF-8")
    child_details = ast.literal_eval(dict_str)
    # TODO verify mother id if exists versus provided JWT
    #print(f'trying to save child details {child_details}')
    postgres_client.add_child(child_details=child_details)
    #print('successfully saved child details')
    return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.OK})


@app.route('/save_woman_details/', methods=['POST'])
@jwt_required()
def save_woman_details():
    # flask.request.files.get('file', '')
    dict_str = request.data.decode("UTF-8")
    woman_details = ast.literal_eval(dict_str)
    # TODO verify mother id if exists versus provided JWT
    postgres_client.add_woman(woman_details=woman_details)
    return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS:ERROR_CONSTS.STATUS_ERROR.OK})

@app.route('/save_file/<child_id>', methods=['POST'])
def save_child_file(child_id):
    #TODO verify that the user is authorised
    file_to_save = flask.request.files.get('uploaded_file_key', '')
    full_path_filename = os.path.join(USERS_DATA_DIR,child_id,file_to_save.filename)
    if os.path.isfile(full_path_filename): #The file exists so output an error
        return jsonify({'status':'file already exists'}),400 #TODO should we let users override their own files?
    os.makedirs(os.path.dirname(full_path_filename),exist_ok=True) #Create directory if doesnt exist
    file_to_save.save(full_path_filename) #Save the file
    return jsonify({'status':'success'})


@app.route('/list_files/<child_id>', methods=['GET'])
def list_child_files(child_id):
    full_data_child_path = os.path.join(USERS_DATA_DIR, child_id)
    if not os.path.isdir(full_data_child_path):
        return jsonify({'files':[]})
    return jsonify({'files':os.listdir(full_data_child_path)})

@app.route('/get_file/<child_id>/<file_name>', methods=['GET'])
def get_child_file(child_id,file_name):
    full_child_file_path = os.path.join(USERS_DATA_DIR, child_id,file_name)
    if not os.path.isfile(full_child_file_path):
        return jsonify({'status': 'no such file found'}),401
    return flask.send_file(full_child_file_path)


    
if __name__ == '__main__':
    app.run(threaded=False, port=9000, host="0.0.0.0", debug=True, )
    # ssl_context=('keys/dordating.crt', 'keys/dordating.key'))