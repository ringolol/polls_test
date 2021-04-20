# User API
## api/v1/active_polls/
Methods: GET

*Get active polls*

```json
Response example:
{
    {
        "id": 1, // poll_id
        "name": "poll-1",
        "start_date": 2020-04-24, 
        "end_date": 2020-05-24, 
        "description": "...",
    },
    ...
}
```


## api/v1/completed_polls_by_user/
Method: POST

*Get polls completed by user*

```json
Request example:
{
    "user_id": 1
}

Response example:
{
    {
        "poll_id": 2,
        "user_id": 1
    },
    ...
}
```

## api/v1/questions_by_poll/
Method: POST

*Get all of the poll's questions*

```json
Request example:
{
    "poll_id": 1
}

Response example:
{
    {
        "id": 1, // question_id
        "poll_id": 2,
        "text": 1,
        "many_answers": true,
    },
    ...
}
```
## api/v1/answers_by_question/
Method: POST

*Get the question answers*

```json
Request example:
{
    "question_id": 1
}

Response example:
{
    {
        "id": 1, // answer_id
        "question_id": 2,
        "text": 1,
    },
    ...
}
```

## api/v1/submit_answers/
Method: POST

*Sumbit answers to the poll*

```json
Request example:
{
    "poll_id": 1,
    "answered_questions": [
        { 
            "question_id": 1, 
            "answers": [ 
                { "answer_id": 1 } 
            ]
        },
        {
            "question_id": 2, 
            "answers": [ 
                { "answer_id": 4 }, 
                { "answer_id": 5 } 
            ]
        }
    ]
}

Response example:
{}
```


# Admin API
## api/v1/add_poll/
Method: POST

*Add a new poll*

```json
Request example:
{
    "poll_name": "some-name",
    "start_date": "2020-12-24",
    "end_date": "2020-12-24",
    "description": "..."
}

Response example:
{}
```

## api/v1/change_poll/
Method: POST

*Change existing poll*

```json
Request example:
{
    "poll_id": 10,
    "updated_pars": {
        "name": "new_name",
        "end_date": "2020-12-25",
        "description": "...?"
    }
}

Response example:
{}
```

## api/v1/delete_poll/
Method: POST

*Delete existion poll*

```json
Request example:
{
    "poll_id": 10
}

Response example:
{}
```

## api/v1/add_question/
Method: POST

*Add a new question to the poll*
```json
Request example:
{
    "poll_id": 2,
    "text": "Be or not to be?",
    "answers": [
        { "text": "be" }, 
        { "text": "not to be" }
    ],
    "many_answers": false
}

Response example:
{}
```

## api/v1/change_question/
Method: POST

*Change existing question*

```json
Request example:
{
    "question_id": 2,
    "updated_pars": {
        "text": "new text",
        "many_answers": true
    }
}

Response example:
{}
```

## api/v1/delete_question/
Method: POST

*Delete existing question*

```json
Request example:
{
    "question_id": 2
}

Response example:
{}
```