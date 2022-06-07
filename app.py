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

app = Flask(__name__)
postgres_client = PostTBD()  # TODO move to app.config

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
    optional_birthday = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.BIRTHDAY.value, None)
    optional_email = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value, None)
    optional_hmo = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.MEDICAL_PROVIDER_NAME.value, None)
    optional_last_period_date = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.LAST_PERIOD_DATE.value, None)
    optional_num_of_pregnancy = request.json.get(SQL_CONSTS.WOMEN_DETAILS_COLUMNS.NUM_OF_PREGNENCY.value, None)
    actual_user_details = postgres_client.get_woman_details(woman_id=username)  # In other apps user_id could be different than username so this might have been different
    if actual_user_details is not None:
        return jsonify({ERROR_CONSTS.STATUS_ERROR.STATUS: ERROR_CONSTS.STATUS_ERROR.USER_ALREADY_EXIST}), 401
    woman_details = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: password,
                     SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value: username,
                     SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value: full_name}
    if optional_birthday is not None or optional_email is not None or optional_hmo is not None or optional_last_period_date is not None or optional_num_of_pregnancy is not None:
        woman_details = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.BIRTHDAY.value: optional_birthday,
                      SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value: optional_email,
                      SQL_CONSTS.WOMEN_DETAILS_COLUMNS.MEDICAL_PROVIDER_NAME.value: optional_hmo,
                      SQL_CONSTS.WOMEN_DETAILS_COLUMNS.LAST_PERIOD_DATE.value: optional_last_period_date,
                      SQL_CONSTS.WOMEN_DETAILS_COLUMNS.NUM_OF_PREGNENCY.value: optional_num_of_pregnancy}

    postgres_client.add_woman(woman_details = woman_details)
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

if __name__ == '__main__':
    app.run(threaded=True, port=9000, host="0.0.0.0", debug=False, )
    # ssl_context=('keys/dordating.crt', 'keys/dordating.key'))