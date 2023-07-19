My Movie API
===

## Install & Dependence
- python 3.8

## Use
- for dev
  ```
  uvicorn main:app --reload
  ```

## Directory Hierarchy
```
|—— config
|    |—— database.py
|—— middlewares
|    |—— error_handler.py
|    |—— jwt_bearer.py
|—— models
|    |—— movieModel.py
|—— routers
|    |—— movie_router.py
|    |—— user_router.py
|—— schemas
|    |—— movie_schema.py
|    |—— user_schema.py
|—— services
|    |—— movie_service.py
|—— utils
|    |—— jwt_manager.py
|—— main.py
```