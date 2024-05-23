from src.utils import get_video_from_chat
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

class FlaskBackend:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        CORS(self.app)
        self.PORT = os.environ.get('PORT', 8001)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def serve_index():
            return send_from_directory('static', 'index.html')

        @self.app.route('/static/<path:path>')
        def serve_static(path):
            return send_from_directory('static', path)

        @self.app.route('/get-video-from-chat', methods=['POST'])
        def chat_with_avatar():
            data = request.get_json()
            message = data['input']
            video_url = get_video_from_chat(message)
            return {'video_url': video_url}

    def run(self):
        self.app.run(host="0.0.0.0", port=self.PORT, debug=True)

if __name__ == "__main__":
    FlaskBackend().run()
