from service.app.factories import create_api
from service.db.migrations import run_migrations

run_migrations()
api = create_api()
