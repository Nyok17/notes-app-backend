1. Project Title
#Notes App

2. Description
A simple note taking backend built with Python flask and SQL. Users are able register, log in, and manage personal notes


3. Demo
It is integrated with frontend(React) and it is live on Vercel = https://notes-app-six-kappa-92.vercel.app
Backend is running on heroku at = https://notes-app1738-8a7df68e8a41.herokuapp.com


5. Features
##Features
-🔒 User authentication with JWT
-🗒️ Add, edit and delete notes
-🌐 REST API backend using Flask + SQLite(Local machine) and postgreSQL on heroku
-📦 Deployed backend on heroku and frontend on Vercel


6. Tech Stack
## Tech Stack
**Frontend:** React, TailwindCSS  
**Backend:** Flask, SQLAlchemy, SQLite  
**Auth:** JWT, bcrypt


6. Getting started
### Backend
1. `Notes App`
2. `pip install -r requirements.txt`
3. `python main.py`


7. API Reference
## API Endpoints

### POST /register
Create a new user.

### POST /login
Login and get a JWT.

### GET /notes
Add notes, Get all notes for the user.


8. Contributing
## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.



9. License
## License

[MIT](LICENSE)



10. Acknowledgements
## Acknowledgements

- Heroku for deployment
- JWT and Bcrypt for Authorization features
- Flask & SQLAlchemy



