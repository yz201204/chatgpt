from flask import Flask
from views.chatGPT_api import chat_gpt_api

app = Flask(__name__)
app.register_blueprint(chat_gpt_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
