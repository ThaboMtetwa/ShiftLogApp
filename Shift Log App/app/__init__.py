from flask import Flask
from app.db import Base, engine, session
from app.routes import index, add_worker, add_shift, export_workers_csv, export_shifts_csv, shift_results, export_worker_shifts_csv
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(Config)  # Load configuration from config.py

    # Create database tables (development only)
    if app.config.get('ENV') == 'development':
        Base.metadata.create_all(engine)

    # Attach session lifecycle management
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    # Register routes with the app
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add_worker', 'add_worker', add_worker, methods=['GET', 'POST'])
    app.add_url_rule('/add_shift/<int:worker_id>', 'add_shift', add_shift, methods=['GET', 'POST'])
    app.add_url_rule('/export/workers_csv', 'export_workers_csv', export_workers_csv)
    app.add_url_rule('/export/shifts_csv', 'export_shifts_csv', export_shifts_csv)
    app.add_url_rule('/shift_results/<int:shift_id>', 'shift_results', shift_results)

    # Register the export worker shifts route:
    app.add_url_rule('/export_worker_shifts_csv/<int:worker_id>',
                     'export_worker_shifts_csv',
                     export_worker_shifts_csv)

    return app
