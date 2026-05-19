from database import engine, Base
import model

## Create the database tables mentioned in the model.py file
Base.metadata.create_all(bind=engine)