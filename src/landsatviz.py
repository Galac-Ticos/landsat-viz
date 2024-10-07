import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from data_ingestion.proxy import Proxy

load_dotenv()

NASA_PASSWORD = os.getenv('NASA_PASSWORD')
NASA_USERNAME = os.getenv('NASA_USERNAME')

app = Flask(__name__)
proxy = Proxy(NASA_USERNAME, NASA_PASSWORD)


@app.route("/",methods=['GET'])
def root():
    return "ok"

@app.route("/search", methods=['GET'])
def search():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    max_cloud_cover = request.args.get('threshold', type=int)
    start_date = request.args.get('startdate', type=str)
    end_date = request.args.get('enddate', type=str)
    # RETURN DATA_TRANSFORMATION
    return jsonify({'succeeded': True})
