from flask import Flask
from views.jira_ding_api import jira_ding_api

app = Flask(__name__)
app.register_blueprint(jira_ding_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
