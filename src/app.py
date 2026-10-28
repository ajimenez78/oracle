from dotenv import load_dotenv
from flask import Flask, jsonify, make_response
import boto3
import os

load_dotenv(override=True)
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = os.getenv('AWS_BEARER_TOKEN_BEDROCK')

app = Flask(__name__)
llm_client = boto3.client("bedrock-runtime", region_name="eu-south-2")

@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.route("/bedrockTest")
def bedrock_test():
    response = llm_client.converse( 
        modelId="eu.anthropic.claude-haiku-4-5-20251001-v1:0", 
        messages=[ 
            { 
                "role": "user", 
                "content": [{"text": "Write a one-sentence bedtime story about a unicorn."}]
            } 
        ] 
    )  

    return response["output"]["message"]["content"][0]["text"]


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
