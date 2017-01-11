# gns3-documentation-template

This repository is use for storing the template and documentation generator for
the GNS3 documentation.


# Test the template

```
pip3 install jinja2
bash server.sh
```

# Documentation generation

The documentation will be export from  google drive folder to a static html site.

If a folder start with a . it will be ignored at export.

## Setup

The generation require Python 3 and the dependencies from requirements.txt.

For easiest usage the run.sh script will spawn a Docker container and run the
script inside.

Next:

* create an application https://console.developers.google.com/?pli=1
* create credentials https://console.developers.google.com/apis/credentials
* download credentials an rename it to client_secret.json

After that create a folder in google drive and put the file you want to export inside.

Create a configuration file configs/test@gmail.com.json:

```
{
    "title": "Test documentation",
    "user_id": "test@gmail.com",
    "folder_id": "2B63b0AONLa3RY1pyRJMxRU0wSzg"
}
```
user_id is your google account and folder id is the id of the folder in google drive

## Run the export

The first export will ask you for credentials. After putting the credentials you need
to run the script again.

Via docker
```
./run.sh python main.py configs/test@gmail.com.json build/
```

You can regenerate only one document
```
./run.sh python main.py configs/test@gmail.com.json build/ DOCUMENT_ID
```

## Running test

```
./run.sh py.test
```
