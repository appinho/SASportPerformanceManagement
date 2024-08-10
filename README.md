# SASportPerformanceManagement
Garmin data capture, integration, visualization, and analytics

## Webpage

http://appinho.pythonanywhere.com/

## Stack
- Front end: Flask
- Back end: Python
- Server: Pythonanywhere

## Commands

```
pip freeze > requirements.txt
flask shell
source .virtualenvs/env/bin/activate
du -sh .virtualenvs/env/lib/python3.10/site-packages/* | sort -hr | head
du -sh venv/lib/python3.10/site-packages/* | sort -hr | head
```

## Setup

```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Dev

```
python3.10 -m venv dev
source dev/bin/activate
pip freeze > requirements.txt
```

## Resources
* https://www.youtube.com/watch?v=5jbdkOlf4cY&ab_channel=PrettyPrinted
* https://prettyprinted.com/courses/flask-sqlalchemy-basics
* https://www.youtube.com/watch?v=8iWJGLtV0aY&list=PLulvxiMryHNoqCRBEAe585OHA85n_ihI_&ab_channel=homastudio