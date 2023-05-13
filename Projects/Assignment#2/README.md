# Assignment 2: Integrate VNET with flask web app

# Run This Application
1. Using Terminal:
- Open a Terminal.
- Move to `~/DevOPS-Career-Track-Poridhi/Projects/Assigment#2/`
- Enter following commands
```commandline
$ export flask_application=app.py
$ flask run
```
You should see output as below - 
```text
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

2. Using Pycharm
- Open the project in Pycharm
- Run `app.py`

# Verify 
- Go to your web browser.
- Paste `http://127.0.0.1:5000` on URL location.
- You should see output on browser as below -
```text
! Hello From Namespace Manager!
Following Are The API list for NameSpace -
Create an NS- /app/create_ns/
Delete a specific NS- /app/delete_ns/
Delete All NS of a User- /app/delete_all_ns_by_user/
Delete All NS - /app/delete_all_ns/
Show All NS- /app/show_all_ns/
Show All NS of a User- /app/show_all_ns_by_user/
```