# What is FastApi

**FastAPI** is a web framework for building APIs quickly and easily with Python. It uses **type hints** to automatically check and process your data, and it creates **interactive documentation** for your API so you can test it right in your browser.


# Setup for FastApi

To install fastapit run this command in your VS-Code Terminal

    pip install "fastapi[standard]"

it installs fastapi and some optional dependencies 

if you do not want the dependencies use pip install fastapi instead 

# Using FastApi

now you can create your python file 'filename.py' and if you want to run it you need to use this command

    fastapi dev filename.py

now you can access your api in your browser using
    
    http://127.0.0.1:8000

or
    
    localhost:8000

A useful tool are the automatic Interactive API docs using Swagger UI and ReDoc allowing you to test and explore your endpoints in a web interface by visiting

    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/redoc
