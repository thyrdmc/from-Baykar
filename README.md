# From BAYKAR
This is a repository containing the source code of the project developed for the Baykartech exam.

## Getting Started

#### Clone the Repo

```git
$ git clone https://github.com/thyrdmc/from-Baykar.git
```

#### Running locally Backend

To secure the project, you should create an .env file in the root directory and store the requirements there. 

```git
DATABASE_HOST=
DATABASE_PORT=

SECRET_KEY=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASS=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

```git
$ cd from-Baykar  # Create a virtualenvironment named venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd fromBaykar
$ python manage.py makemigrations
$ python manage.py migrate
```

For Accessing Admin Panel
```git
$ python manage.py createsuperuser
```
and Running Locally
```git
$ python manage.py runserver
```

Open http://127.0.0.1:8000/ with your browser to see the result.

Please refer to the documentation via Postman to access and test the APIs of the program running locally.

https://www.postman.com/telecoms-engineer-26513248/workspace/frombaykar-documentation/collection/30810325-5c8ded97-1a8b-4c84-9b75-d068bf53218c?action=share&creator=30810325

#### Running locally Frontend
```git
$ cd from-Baykar  (Root Directory)
$ source venv/bin/activate
$ cd fromBaykar-frontend
$ npm run dev
```
#### Built With
* Django (Backend) & PostgreSQL => Completed
* React & JavaScript (Frontend) => In Progress
