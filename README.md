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
## Environment variable
## API definition
### Current User related

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* [Show info] : `GET /api/user/`
* [Update info] : `PUT /api/user/`

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

| Age           | Time  | Food | Gold |
| ------------  | ----  | ---  | ---  |
| Feudal Age    | 02:10 |  500 |    0 |
| Castle Age    | 02:40 |  800 |  200 |
| Imperial Age  | 03:30 | 1000 |  800 |

- Pairs

| Age           | Time  | Food | Gold |
| ------------  | ----  | ---  | ---  |
| Feudal Age    | 02:10 |  500 |    0 |
| Castle Age    | 02:40 |  800 |  200 |
| Imperial Age  | 03:30 | 1000 |  800 |

## How to implement IP request check


| Hash name                           | count             | reset         |
| ----------------------------------  | ----------------- | ------------- |
| API URL + API Method + IP adress    | Amount of request |  Expired time |

\*   Maximum is 10. If expired, it will re-zero.\
\**  If expired time < current time, it will be reset to *current time + 1 hour*


