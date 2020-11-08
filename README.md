# rate-limit

A dockerized flask app combined with JWT, postgreSQL and redis. 
It use redis to record the amount of request and set X-rate-limit in the response header. If exceed the limit, it will send HTTPstatus 429.

## Prerequisite
- Flask
- PostgreSQL
- Redis
- Lua

## Get started

## DB structure
