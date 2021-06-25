# Full Stack API Final Project


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

### Local setup
* **Pre-requisites**<br>
Developers using this project should already have Python3, pip and node installed on their local machines. The frontend depends on Nodejs and Node Package Manager (NPM).

* **Start your virtual environment**<br>
From the backend folder run
```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

* **Install dependencies**

From the backend folder run 
```bash
# All required packages are included in the requirements file. 
pip3 install -r requirements.txt
# In addition, you will need to UNINSTALL the following:
pip3 uninstall flask-socketio -y
```
From the frontend folder run 
```bash
# Install project dependencies
npm install
```

* **Start local environment**

From the backend folder, start the server 
```bash
FLASK_APP=flaskr FLASK_ENV=development flask run --reload
```
From the frontend folder run 
```bash
# Install project dependencies
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## Project Endpoints

```js
GET '/categories'
- Fetches an array of categories, each category has the keys: id, an integer and type, the label string of the category
- Request Arguments: None
- Returns: An object with the following keys: success, of boolean type, and categories, that contains an array of category objects. 
{
    success: true,
    categories: [
        {
            id: 1,
            type: "Science"
        },
        ...
    ]
}
```


```js
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with keys: success, of type boolean, questions, the current page questions, max. 10 questions, total questions, an integer, an array of all categories, and the current category id.
{
    success: true,
    questions: [
        {
            id: 1,
            question: "This is a question",
            answer: "This is an answer", 
            difficulty: 5,
            category: 2
        },
        ...
    ],
    totalQuestions: 100,
    categories: [
        {
            id: 1,
            type: "Science"
        }
        ...
    ],
    currentCategory: None
}
```

```js
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with keys: success, of type boolean, an array with questions for the specified category, total questions, and current category id.
{
    success: true, 
    questions: [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
        ...
    ],
    totalQuestions: 100,
    currentCategory: 8
}
```

```js
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: An object with key success, of type boolean. Besides, it returns the appropriate HTTP status code. 
```

```js
POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{
    previous_questions: [], // an array with ids of questions such as [1, 4, 20, 15]
    quiz_category: an object of the current category
}
- Returns: an object with keys: success, of type boolean, and a single new question. object 
{
    success: true, 
    question: {
        id: 1,
        question: 'This is a question',
        answer: 'This is an answer', 
        difficulty: 5,
        category: 4
    }
}
```

```js
POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
{
    question: 'Heres a new question string',
    answer: 'Heres a new answer string',
    difficulty: 1,
    category: 3
}
- Returns an object with keys: success, of type boolean, created, an integer representing the id of the created question, the questions, paginated, as well as the updated total number of questions: 
{
    success: true,
    created: 1,
    questions: [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
        ...
    ],
    totalQuestions: 100,
}
```

```js
POST '/questions'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: an object with keys: questions, an array of the matching questions paginated, a number of totalQuestions that met the search term and the current category string. 
{
    questions: [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
        ...
    ],
    totalQuestions: 100,
    currentCategory: None
}
```