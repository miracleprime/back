from models import app
from routes import app # Import the app from models.py
from models import app, db, Route
import json

if __name__ == '__main__':
    app.run(debug=True)

