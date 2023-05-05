import json
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
import redis
import os

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int

def get_redis_connection():
    REDIS_HOST = os.environ.get("REDIS_HOST")                      
    REDIS_PORT = os.environ.get("REDIS_PORT")                              
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return redis_conn

@app.post("/register/")
def register(user: User, redis_conn: redis.Redis = Depends(get_redis_connection)):
    user_json = json.dumps(user.dict())
    redis_conn.hset("users", user.id, user_json)
    return {"message": "User registered successfully", "user": user}

@app.get("/users/{user_id}", response_model=Optional[User])
def get_user(user_id: int, redis_conn: redis.Redis = Depends(get_redis_connection)):
    user_json = redis_conn.hget("users", user_id)
    if user_json is None:
        return None
    return json.loads(user_json)

@app.get("/users/", response_model=List[User])
def get_users(redis_conn: redis.Redis = Depends(get_redis_connection)):
    users = []
    user_ids = redis_conn.hkeys("users")
    for user_id in user_ids:
        user_json = redis_conn.hget("users", user_id)
        users.append(json.loads(user_json))
    return users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
