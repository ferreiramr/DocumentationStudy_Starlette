from starlette.applications import Starlette
from starlette.config import Config
import databases

config = Config(".env")

TESTING = config('TESTING', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
TEST_DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)

# Use 'force_rollback' during testing, to ensure we do not persist database changes
# between each case.

if TESTING:
    database = databases.Database(TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(DATABASE_URL)