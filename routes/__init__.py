from .user_routes import user_bp
from .admin_routes import admin_bp

def init_routes(app):
    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')
