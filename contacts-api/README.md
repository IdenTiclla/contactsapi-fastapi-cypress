# Contacts-api (Fastapi Project)
This is the Fastapi project used for building the api that will be tested with cypress later.

# Requirements
For running this Fastapi project you need to have python installed, you can check if you have python installed.

```sh
    python --version
```
Once you have python installed on your machine then you will have pip installed automatically
You can check pip installation:
```sh
    pip --version
```

Once you have python and pip you need to installing the fastapi project.

# Installation
For running this project you need virtualenv

```sh
    pip install virtualenv
```

With virtualenv installed we can create our separated environment:

```sh
    python -m virtualenv venv
```

Once you created your separated environment you need to activate it:
For ubuntu you can run this:
```sh
    source venv/bin/activate
```
For windows or mac check on the virtualenv documentation

Once the separated environment is activated you need to install the dependencies:
```sh
    pip install -r requirements.txt
```

# Running the project
```sh
    fastapi dev main.py
```