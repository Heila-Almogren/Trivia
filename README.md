# Trivia API

#### Trivia API provides you with quiz questions on different categories.. wether in science, history, sport, art, geography or entertainment, you also can add a new a question in any category, or delete it if needed.


## Getting started: Preparing local environment
### Backend

first of all, you have to install the required dependencies:

1- navigate to the backend folder

2- run ``` pip install requirements.txt ```. 

3- After that you'll be able to run the application:<br />
``` export FLASK_APP=flaskr``` <br />
```FLASK_ENV=development``` <br />
```FLASK_DEBUG=true ```


### Frontend
After that navigate to front folder and run ```npm start```. after that the application will run on http://localhost:3000/.

## Database preparation
To be able to use the application directly, import the already created psql file by running ```psql trivia < trivia.psql```.

## API Reference

### GET /categories
returns a success flag, list of categories objects and the total number of categories. example:
* example: ```curl -X GET http://localhost:3000/categories``` <br />
 `` {"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"},"success":true,"total_categories":6} ``



### GET /questions

# POST

### Errors
#### 404: Not Found:
Means that the resource is currently unavailable and can't be found in the server.
#### 422: Unprocessable:
Means that request is understood by the server, however for some reason it cannot be processed.
#### 400: Bad request:
Means that the request cannot be processed by the server due to a client side problem, such as syntax or invalid request.
#### 405: method not allowed:
Means that the requested method is not allowed to processed to the specified resource.
#### 500: Server error:
Means that the requested method could not be processed due to a server error problem.

## Tests
You can run test bt running the unit test file using ```Python3 test_flaskr.py```.






