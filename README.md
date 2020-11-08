# rate-limit

  A dockerized flask app combined with JWT, postgreSQL and redis. 
It use redis to record the amount of request and set X-rate-limit in the response header. If exceed the limit, it will send HTTPstatus 429.

## Prerequisite
- Flask
- PostgreSQL
- Redis
- Lua

## Get started
```
# Clone project
git clone

# Build the image 
cd <project directory>
./build.sh

# Run docker compose to create contain
docker-compose up --build
```

## API definition

### Pair related

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* Show info   : `GET /api/user/`
* Update info : `PUT /api/user/`

### Current User related

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* Show info   : `GET /api/user/`
* Update info : `PUT /api/user/`

### Account related

Endpoints for viewing and manipulating the Accounts that the Authenticated User
has permissions to access.

* Show Accessible Accounts : `GET /api/accounts/`
* Create Account : `POST /api/accounts/`
* Show An Account : `GET /api/accounts/:pk/`
* Update An Account : `PUT /api/accounts/:pk/`
* Delete An Account : `DELETE /api/accounts/:pk/`

## DB structure
- Users

| Column name     | Type      | 
| --------------- | --------- |
| id              | uuid      | 
| email           | char      |             
| name            | char      |         
| password_digest | char      |      
| modified_time   | timestamp |      
| created_time    | timestamp |     

- Pairs

| Column name   | Type  |
| ------------  | ----  |
| user_id_one   | uuid  |
| user_id_two   | uuid  |

## How to implement IP request check

| Hash name                           | count             | reset         |
| ----------------------------------  | ----------------- | ------------- |
| API URL + API Method + IP adress    | Amount of request |  Expired time |

\*   Maximum is 10. If expired, it will re-zero.\
\**  If expired time < current time, it will be reset to *current time + 1 hour*


