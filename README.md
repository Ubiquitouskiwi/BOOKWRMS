# BOOKWORMS

This is a home library system to keep track who you lend books to as well as keep track of what books you have. BOOKWORMS stands for  "Becca's Online Organized Knowledge Warehouse and Resource Management System."

## Dev Setup
>Tutorial that was followed: https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/

1. Install python 3.11 from the Micrsoft store:

>https://www.microsoft.com/store/productId/9NRWMJP3717K


2. Install Visual Studio Code (vs code) from here:

>https://code.visualstudio.com/


3. Create a folder somewhere on your local machine that will house this project and virtual environment (venv). Ex:

```
C:\Users\{user}\Documents\PythonProjects
```

4. Open folder above in vs code and open a terminal inside vs code. On the left hand side look for "source control" and pull this project and switch to that project folder.

5. Create your venv using the venv library native to python. run the following command in the vs code terminal:

 ```
 python -m venv venv
 ```
 >ps. the second venv above is the name of the virtual environment. it can be anything you like, but make sure you remember it

6. Activate virtual environment by running Activate.ps1 in the venv/Scripts/ folder. Ex:

```
& venv/Scripts/Activate.ps1
```

7. Install all required libraries listed in the requirements.txt

```
pip install {python-library}
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
