SETUP:
1- install virtualenv
    - "pip3 install virtualenv"

2- create/activate virtualenv :
    create :
        "virtualenv venv"

    activate:
        "source task/bin/activate"

3- install packages mentioned in requirement.txt:
    - "pip3 install -r requirement.txt"

4-update environment file (.env)

5- create database named "url_db" in mysql database.
    4.1- migrate changes:
        make migrate

        or

        python3 manage.py makemigrations 
        python3 manage.py migrate


6 - start app using command:  
            'make start' 
                or 
            python3 manage.py runserver

7-  go to url "http://localhost:8000/swagger/" for testing

END_POINTS:
    <HOST_URL>/api/   - list of all mapping in database
    <HOST_URL>/api/create   - create shortURL from a valid url
    


