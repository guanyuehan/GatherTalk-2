from flask import Flask
from routes.chat_routes import chat_bp  # Import your chat blueprint
import os

app = Flask(__name__)

app.register_blueprint(chat_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(host='0.0.0.0', port=port)