from app import create_app
from app.extensions import db
import os



app = create_app()



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Heroku's port or fallback to 5000
    app.run(host='0.0.0.0', port=port)