from auth_database import engine, Base
import models

## Create the database tables mentioned in the models.py file
Base.metadata.create_all(bind=engine)