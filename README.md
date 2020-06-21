# CSB_App
This is a calendar slot booking app which is based on ```flask``` (A micro framework in python).

## Installation
Install all the required modeules.

```Flask```
```flask_mysqldb```
```wtforms```
```functools```
```Passlib```

## Create database
To store the user's data, Create a Database ```navigus``` 
and create two Tables in it:
## 1) users
using given command in mysql
```CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), username VARCHAR(130), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);```

## 2) meetings
using given command in mysql
```CREATE TABLE meetings(id INT(10) AUTO_INCREMENT PRIMARY KEY, title VARCHAR(100),day VARCHAR(10),month VARCHAR(10),time VARCHAR(100), user VARCHAR(100));```

## How to run
To use the application, Run the app.py file.


