from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
import os

def create_app():
    # Angular 17+ defaults to dist/project-name/browser
    dist_folder = os.path.abspath(os.path.join(os.getcwd(), 'frontend/dist/frontend/browser'))
    
    # Disable default static serving to avoid conflicts
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app)
    db.init_app(app)

    # Import Blueprints
    from routes.auth_routes import auth_bp
    from routes.company_routes import company_bp
    from routes.location_routes import location_bp
    from routes.data_routes import data_bp
    from routes.admin_routes import admin_bp
    from routes.driver_routes import driver_bp
    from routes.public_routes import public_bp
    from routes.client_routes import client_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(company_bp, url_prefix='/api/company')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(driver_bp, url_prefix='/api/driver')
    app.register_blueprint(location_bp, url_prefix='/api/location')
    app.register_blueprint(public_bp, url_prefix='/api/public')
    app.register_blueprint(client_bp, url_prefix='/api/client')

    @app.route('/uploads/banners/<path:filename>')
    def serve_banner(filename):
        uploads = os.path.join(os.getcwd(), 'uploads', 'banners')
        return send_from_directory(uploads, filename)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_static(path):
        # API calls should already be handled by blueprints, but just in case:
        if path.startswith('api/'):
            return "API Endpoint Not Found", 404
            
        # Serve file if exists
        file_path = os.path.join(dist_folder, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
             return send_from_directory(dist_folder, path)
             
        # SPA Fallback for non-API routes
        return send_from_directory(dist_folder, 'index.html')

    # Background Job for Expired Reservations
    import threading
    import time
    from sqlalchemy import text

    def run_schedule():
        while True:
            try:
                with app.app_context():
                    # Check for expired reservations
                    # User asked for 'after 5 min'.
                    # This script runs every minute to clean up anything older than 5 mins.
                    # print("Running automated reservation cleanup...")
                    db.session.execute(text("EXEC sp_CancelarReservasExpiradas"))
                    db.session.commit()
            except Exception as e:
                print(f"Scheduler Error: {e}")
            time.sleep(60) # Run every minute

    # Start independent thread
    scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
    scheduler_thread.start()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
