from dotenv import load_dotenv
from flask import Flask, jsonify, make_response
from openai import OpenAI  
import os

load_dotenv(override=True)
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_BASE_URL'] = os.getenv('OPENAI_BASE_URL')


app = Flask(__name__)

llm_client = OpenAI()

@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.route("/bedrockTest")
def bedrock_test():
    response = llm_client.responses.create( 
        model="openai.gpt-oss-120b", 
        input=[ 
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."} 
        ] 
    )  

    return response.output_text


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
