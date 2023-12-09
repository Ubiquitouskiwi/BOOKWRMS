# BOOKWRMS

[![License](https://img.shields.io/badge/license-AGPL-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Flask](https://img.shields.io/badge/flask-3.0-brightgreen.svg?logo=flask)](https://flask.palletsprojects.com/en/3.0.x/)
[![Python](https://img.shields.io/badge/python-3.11-orange.svg?logo=python)](https://www.python.org/)

![Screenshot](doc_files/Screenshot_2023-12-08_210654.png|width=50)

This is a home library system to keep track who you lend books to as well as keep track of what books you have. BOOKWRMS stands for  "Becca's Online Organized Knowledge Warehouse and Resource Management System."

## Dev Setup
>Tutorial that was followed: https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/

1. Install python 3.11 from the Micrsoft store:

>https://www.microsoft.com/store/productId/9NRWMJP3717K


2. Install Visual Studio Code (vs code) from here:

>https://code.visualstudio.com/


3. Create a folder somewhere on your local machine that will house this project and virtual environment (venv). Ex:

Windows:
```Windows
C:\Users\{user}\Documents\PythonProjects
```
Linux:
```Linux
/home/Documents/projects/python
```

4. Open folder above in vs code and open a terminal inside vs code. On the left hand side look for "source control" and pull this project and switch to that project folder.

5. Create your venv using the venv library native to python. run the following command in the vs code terminal:

Windows:
 ```Windows
 python -m venv venv
 ```
 Linux (May neet to install with apt install python3.11-venv)
 ```Linux
 python3 -m venv venv
 ```
>ps. the second venv above is the name of the virtual environment. it can be anything you like, but make sure you remember it

6. Activate virtual environment by running Activate.ps1 in the venv/Scripts/ folder. Ex:

Windows:
```Windows
& venv/Scripts/Activate.ps1
```
Linux:
```Linux
source venv/bin/activate
```

7. Install all required libraries listed in the requirements.txt

```
pip install -r requirements.txt
```

8. Initialize and create and fill the local DB using command:

```
flask --app flaskr init-db --dev true
```
>ps use this command for blank DB: ```flask --app flaskr init-db``` 

9. Run the flask app locally with this command

```
flask --app flaskr run --debug
```

# Architecture
![Architecture Diagram](https://github.com/Ubiquitouskiwi/BOOKWORMS/blob/master/doc_files/BOOKWORMS_architecture.drawio.svg)
