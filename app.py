from flask import Flask
from flask import request
from flask import Response
from src.source import insert_csv_to_db, check_table, query_data, truncate_table
from io import StringIO
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload/<table>',methods=['POST'])
def upload_table_api(table):

    if check_table(table):
        if "csv_data" in request.files: 
            csv_data = request.files["csv_data"]
            file_bytes = csv_data.stream.read()
            content = file_bytes.decode()
            file_stream = StringIO(content)

            logs = insert_csv_to_db(table, file_stream)

            response = Response(
                response=json.dumps({"messages":logs}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({"message":"Missing parameter 'csv_data' in Multipart body".format(table)}),
                status=400,
                mimetype='application/json'
            )
    else:
        response = Response(
            response=json.dumps({"message":"Table {0} does not exist".format(table)}),
            status=404,
            mimetype='application/json'
        )
    return response

@app.route('/truncate/<table>',methods=['DELETE'])
def truncate_table_api(table):
    if check_table(table):
        logs = truncate_table(table)
        
        response = Response(
            response=json.dumps({"messages":logs}),
            status=200,
            mimetype='application/json'
        )
    else:
        response = Response(
            response=json.dumps({"message":"Table {0} does not exist".format(table)}),
            status=404,
            mimetype='application/json'
        )
    return response

@app.route('/query/<query>/<year>',methods=['GET'])
def get_results(query, year):
    
    query_result = query_data(query,year)

    response = Response(
            response=query_result,
            status=200,
            mimetype='application/csv'
        )
    
    return response


app.run(host="0.0.0.0")
