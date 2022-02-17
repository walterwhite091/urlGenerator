#### LOCAL SETUP
1. Install virtualenv
      `pip3 install virtualenv`

2. create/activate virtualenv
   - create 
        `virtualenv venv`

    - activate:
        `source venv/bin/activate`

3.  Install packages mentioned in requirement.txt:
    - `pip3 install -r requirements.txt`

4.  Update environment file (.env)
    -`source .env`

5. create database named <DB_NAME> same as metioned in environment file in mysql database.
    -`CREATE DATABASE <DB_NAME> `   
6. Migrate changes
    -`make migrate`
or
    -`python3 manage.py makemigrations && python3 manage.py migrate` 
        
7. Start app  
    -`make start` 
    or 
    -`python3 manage.py runserver`

7-  GO TO URL "http://localhost:8000/swagger/" for testing

---

#### END_POINTS:
    <HOST_URL> - html page rendered with a simple  user-friendly form input
    <HOST_URL>/url/   - support [GET,POST] - use POST to create new URL and GET to receive list of all URLS in DB.
    <HOST_URL>/url/<id>

---
#### ENVIRONMENT FILE
- HOST_IP=127.0.0.1     
- HOST_PORT=8000
- HOST_URL=${HOST_IP}:${HOST_PORT}

- DB_NAME='short_urls'
- DB_USER='' 
- DB_PASSWORD=''




    


