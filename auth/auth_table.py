from auth.auth_database import engine, Base
from auth import models

## Create the database tables mentioned in the models.py file
Base.metadata.create_all(bind=engine)