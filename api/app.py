from flask import Flask, send_from_directory
from flask_cors import CORS
from api.routes import api_blueprint
import os

def create_app():
    app = Flask(__name__, static_folder="../client/build", static_url_path="/")
    CORS(app)

    # Register the API blueprint
    app.register_blueprint(api_blueprint)

    # Serve the React index.html for the root route
    @app.route("/")
    def serve_index():
        return send_from_directory(app.static_folder, "index.html")

    # Catch-all for React Router (e.g., /dashboard or other frontend routes)
    @app.errorhandler(404)
    def fallback(e):
        return send_from_directory(app.static_folder, "index.html")

    return app

# Run the Flask app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000, host="0.0.0.0")
