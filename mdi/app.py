#!/usr/bin/env python

from json import dumps as json_dumps
from socket import gethostname
from boto3 import client as boto3_client
from flask import Flask, jsonify, request, make_response
from datetime import datetime
from mdi import __version__
from mdi import config


# Setup Flask application
app = Flask(__name__)
app.config.from_envvar('FLASK_SECRETS')

@app.route('/', methods=["GET", "POST"])
def index():
    now = datetime.now()

    if request.method == "POST":

        if not request.data:
            return render_result(400, "error", "No JSON data provided")

        json_data = request.get_json()
        json_data["timestamp"] = int(now.timestamp())
        json_data["datestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
        if not json_data.get("device_name"):
            json_data["device_name"] = gethostname()

        print(f"Using payload: {json_data}")

        publish_kinesis(config.STREAM_NAME, config.REGION, json_data, json_data["device_name"])
        write_fs(config.DATA_PATH, json_data["timestamp"], json_data)

        return render_result(202, "success", "Data stored for processing")
    else:
        return render_result(200, "success", "Welcome")


def render_result(code, status, message):
    response = make_response(jsonify({
        "status": status,
        "message": message,
        "app": config.APP_NAME,
        "version": __version__
    }), code)
    return response

def write_fs(path, name, data):
    fs_path = f"{path}/{name}.json"
    print(f"Writing payload to {fs_path}")
    with open(fs_path, "w") as f:
        f.write(json_dumps(data))
    print("Payload written to filesystem")

def publish_kinesis(stream, region, data, pk):
    print("Publishing payload to Kinesis")
    kinesis = boto3_client("kinesis", region_name=region)
    res = kinesis.put_record(
        StreamName=stream,
        Data=json_dumps(data),
        PartitionKey=pk
    )
    print(f"Kinesis response: {res}")

if __name__ == "__main__":
    app.run()
