# Calculator Api

This template includes samples how to install the application and documentation about the endpoints.

First of all I am using  Python and Serverless Framework to build the application.

## Environment Information
Domain: https://o01xgqczze.execute-api.us-east-1.amazonaws.com
Credentials
```
{
    "username":"payorayo@gmail.com",
    "password":"Password123$"
}
```

## Install

Setup your amazon credential in your credentials file [official documentation](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/)

```bash
Run the following command in root path
$ npm install
$ serverless deploy

Deploying calculator-api to stage dev (us-east-1)

✔ Service deployed to stack calculator-api-dev (170s)

```

## Accounts
I am using AWS Cognito like service to store the password, generate tokens. First you need to create an account after 
generate new auth token. With that auth token, you can consume remaining endpoints.

### Create Account

```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"<EMAIL>",
    "password":"<PASSWORD>",
    "user_balance": <USER_BALANCE>
}
'
response 
{
    "message": "There is an account with that username"
}
'
```

_Note_: User Balance numeric or decimal positive value and all fields are required


### Get Auth Token
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"<EMAIL>",
    "password":"<PASSWORD>"
}
'
response
{
    "token": "<TOKEN>"
}
```
_Note_: All fields are required

### Edit Account

You just can update `user_balance`.

```bash
curl --location --request PUT 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/user' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJraWQiOiJNTkJrOGRzUWxqeldVelR2NWlsWVJIWVwvK3R4bkk2NHVwbUxzbkRla2Zzaz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1ZThmZWU2My02NDNhLTRhMWEtYmY2MC05OGZiZjA1NDA2YjIiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3dHbklFd0VBeiIsImNvZ25pdG86dXNlcm5hbWUiOiI1ZThmZWU2My02NDNhLTRhMWEtYmY2MC05OGZiZjA1NDA2YjIiLCJvcmlnaW5fanRpIjoiM2JjNzE4OWYtNzRlOC00NWFiLTllZTktMDQ1NGU3MzM4ZTdhIiwiYXVkIjoiNG9jbjhnMzRmMWJzZGZqdG92dGU0MXJuaDEiLCJldmVudF9pZCI6IjhjZmNiMTMyLWVmZTQtNDhjNy04ZDkxLTQxMjM3Njk3YmZlMiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjgxMzE4NzQ2LCJleHAiOjE2ODE0MDUxNDYsImlhdCI6MTY4MTMxODc0NiwianRpIjoiODBlN2U5NGItMTA1Mi00OWFiLWFiNmYtNzVkNDZjNThhNGIwIiwiZW1haWwiOiJwYXlvcmF5b0BnbWFpbC5jb20ifQ.bOAnkp8zbjBLSQ9oMxkCW5wxwnzpHhpNBx9DEqg__w6fpUO0-yhdG3wnaZeZdMfbahbvMRZJIOq3ZjzMDNJn_IXuBiQ-C_6vWwODTvibTLAPn92Xy7jXlSxp_umV8vl2FoO1L2jt4NyQUNIcZeuHRmYDTeCqYx19bx94XmmQNffNFWpAqdz7pjIzfBI88mlHomq9MJsqWLlcKO9n-7Bue-jgp8e-i8LDU8y9hPZNyxqAMOombm-U9ZMLlL3k098Om_M1QQMyXaA_nC3YZyd07JZqHKO6qbTz7nRxxa65AtBbim8DvhUzxgrlA92t6OPq82mPiwt5pMjVxzNS9Axkmw' \
--data '{
    "user_balance": <USER_BALANCE>
}
'
Response
{
    "message": "User was updated successfully"
}
```
_Note_: All fields are required

### Account Info
The endpoint gets user information.
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/user' \
--header 'Authorization: Bearer <TOKEN>'

Response
{
    "user_info": {
        "user_id": "zzzzzzzzz",
        "username": "<EMAIL>",
        "user_balance": <USER BALANCE>
    }
}
'
```
_Note_: User id is generated by AWS Cognito directly and all fields are required

### Remove Account
```bash
curl --location --request DELETE 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/user' \
--header 'Authorization: Bearer <TOKEN>'

Response
{
    "message": "User was removed successfully"
}
```
_Note_: The deleted account keeps in dynamodb just changed the status to `inactive` instead of `active`. 
But in the case of Cognito the account is removed because Cognito Pool is connected to Email. 
We can not two accounts with same email in Cognito


## Operation
The application just support the following types:
* addition
* subtraction
* multiplication
* division
* square_root
* random_string

The application does not allow two operations with tha same type and each operation own identifier `operation_id`

### Create Operation
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/operation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "type":"square_root",
    "cost": 500
}
'
Response
{
    "message": "Operation was created successfully"
}
'
```
_Note_: Cost is a numeric or decimal positive value and all fields are required

### List Operation
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/operation/list' \
--header 'Authorization: Bearer <TOKEN>'
'
Response
{
    "operations": [
        {
            "operation_id": "11111",
            "type": "multiplication",
            "user_balance": 300
        },
        {
            "operation_id": "222222",
            "type": "random_string",
            "user_balance": 600
        },
        {
            "operation_id": "333333",
            "type": "addition",
            "user_balance": 100
        },
        {
            "operation_id": "444444",
            "type": "subtraction",
            "user_balance": 200
        },
        {
            "operation_id": "55555",
            "type": "square_root",
            "user_balance": 500
        },
        {
            "operation_id": "66666",
            "type": "division",
            "user_balance": 400
        }
    ]
}
'
```

### Edit Operation
```bash
curl --location --request PUT 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/operation/<OPERATION_ID>' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "cost": 600
}
'
'
Response
{
    "message": "Operation was updated successfully"
}
'
```
_Note_: Cost is a numeric or decimal positive value

## Calculation

### Create Calculation
There is specific request per each operation.

Division
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/calculation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "operation_id": "<OPERATION_ID>",
    "dividend": 9,
    "divisor": 3
}'
'
Response
{
    "operation_type": "division",
    "operation_response": "3.0",
    "user_balance": 3600,
    "operation_cost": 400
}
'
```

Addition
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/calculation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "operation_id": "<OPERATION_ID>",
    "addend_one": 9,
    "addend_one": 3
}'
'
Response
{
    "operation_type": "addition",
    "operation_response": "12.0",
    "user_balance": 3600,
    "operation_cost": 100
}
'
```

Subtraction
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/calculation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "operation_id": "<OPERATION_ID>",
    "minuend": 9,
    "subtrahend": 3
}'

Response
{
    "operation_type": "subtraction",
    "operation_response": "6.0",
    "user_balance": 3600,
    "operation_cost": 100
}
'
```

Multiplication
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/calculation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "operation_id": "<OPERATION_ID>",
    "multiplicand": 9,
    "multiplier": 3
}'

Response
{
    "operation_type": "multiplication",
    "operation_response": "27.0",
    "user_balance": 3600,
    "operation_cost": 100
}
'
```

Random String
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/calculation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "operation_id": "<OPERATION_ID>",
    "length_string": 5
}'

Response
{
    "operation_type": "random_string",
    "operation_response": "csew2",
    "user_balance": 3600,
    "operation_cost": 100
}
'
```

square_root
```bash
curl --location 'https://o01xgqczze.execute-api.us-east-1.amazonaws.com/dev/calculation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "operation_id": "<OPERATION_ID>",
    "radicand": 25
}'

Response
{
    "operation_type": "square_root",
    "operation_response": "5,0",
    "user_balance": 3600,
    "operation_cost": 100
}
'
```


### Filter Records
