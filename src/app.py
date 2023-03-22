from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os
import yaml
from src.constant import *
#from src.entity.app_config import appconfig

# Init the Flask App
app = Flask(__name__)

# Initialize the OpenAI API key

ROOT_DIR = os.getcwd()  #to get current working directory
PARAMS_FILE_NAME = "params.yaml"
file_path = os.path.join(ROOT_DIR,PARAMS_FILE_NAME)

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e

config_info  = read_yaml_file(file_path=file_path)
app_config = config_info[APP_CONFIG_KEY]
OPENAI_API_KEY = app_config[OPENAI_API_KEY]
#OPENAI_API_KEY= "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"
openai.api_key = os.environ.get("OPENAI_API_KEY")

completion = openai.ChatCompletion()


start_chat_log = [
    {"role": "system", "content": "Hi there !!"}
]

def askgpt(question, chat_log =None):
    if chat_log is None:
        chat_log = start_chat_log
    chat_log = chat_log + [{'role':'user', 'content': question}]
    response = completion.create(model = 'gpt-3.5-turbo', messages = chat_log)
    answer = response.choices[0]['message']['content']
    chat_log = chat_log + [{'role': 'assistant', 'content': answer}]
    return answer, chat_log


# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = askgpt(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)