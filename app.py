import os
from flask import Flask, render_template, session
from config import Config
from models import db
from models.user import User

# Import Blueprints
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.career import career_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database directory exists if writable
    db_dir = os.path.join(app.root_path, 'database')
    try:
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    except Exception:
        pass

    # Initialize extensions

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(admin_bp)

    # Global context processor
    @app.context_processor
    def inject_user():
        current_user = None
        if 'user_id' in session:
            current_user = User.query.get(session['user_id'])
        return dict(current_user=current_user)

    # Landing Page Route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # Auto create tables if not existing
    with app.app_context():
        db.create_all()
        try:
            from database.mongo_sync import init_mongo_sync, sync_all_existing_data
            init_mongo_sync(db)
            sync_all_existing_data(app, db)
        except Exception as e:
            app.logger.warning(f"MongoDB auto sync initialization warning: {e}")

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
