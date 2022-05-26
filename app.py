
from flask import Flask
from flask import jsonify, request, send_from_directory, redirect
from postgres_client import PostTBD
import ast
import flask
from sql_consts import SQL_CONSTS

app = Flask(__name__)
postgres_client = PostTBD() #TODO move to app.config


@app.route('/hello',methods=['GET'])
def say_hello():
    return jsonify({'response':'hello'})

@app.route('/get_woman_details/<woman_id>')
def get_woman_id(woman_id):
    #TODO security eg make sure that woman_id is accessing it via a session token/JWT
    data = postgres_client.get_woman_details(woman_id=woman_id)
    data = dict(data)
    # if not data[SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value] == 'shira':
    #     return jsonify({'status':'This is not Shira'}),400
    
    # This is how you debug through the console : import ipdb; ipdb.set_trace()
    return jsonify(data)

@app.route('/get_child_details/<child_id>')
def get_child_id(child_id):
    data = postgres_client.get_child_details(child_id=child_id)
    return jsonify(data)

@app.route('/save_child_details/',methods=['POST'])
def save_child_details():
    #flask.request.files.get('file', '')
    dict_str = request.data.decode("UTF-8")
    child_details = ast.literal_eval(dict_str)
    # TODO verify mother id if exists versus provided JWT
    postgres_client.add_child(child_details=child_details)
    return jsonify({'status':'ok'})



if __name__ == '__main__':
    app.run(threaded=False, port=9000, host="0.0.0.0", debug=True,)
            #ssl_context=('keys/dordating.crt', 'keys/dordating.key'))