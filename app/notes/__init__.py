from .routes import notes_bp


def init_notes_module(app):
    app.register_blueprint(notes_bp)

__all__=['notes_bp', 'init_notes_module']