# A simple flask app

## Narrative / outline
This file storage app is an application to storage user's files. Users may upload, delete
download and share thier files.Only logined user can upload,delete and share thier files,
a anonymous user may download the file shared by other user with a access token.


## relational diagram


![relational diagram](./docs/images/relational_diagram.png)

## email/password table

| email          | password |
|----------------|----------|
| a@a.com        | ''       |
| b@a.com        | 123      |
| abcde@a.com    | ''       |


## how to run this app?
python >= 3.7

change the config.DB to your config, create a database named flask_app for your app.

run as a new app:
```shell
$ pip install virtualenv

$ cd my_project_dir

$ virtualenv venv

$ source venv/bin/activate

$ pip install -r requirements.txt

$ mysql -u yourusername -p

MYSQL [flask_app]> source data.sql;

$ python main.py
```

run with records,unzip the local zip file:
```shell
$ cd my_unzip_project_dir

$ mysql -u yourusername -p

MYSQL [flask_app]> source database_export.sql;

$ source venv/bin/activate

$ python main.py
```