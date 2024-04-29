from fastapi import FastAPI, Depends
from routers.tasks import router as tasks_router
from routers.user import getUser, router as user_router

import uvicorn

app = FastAPI()

app.include_router(user_router, tags=["users"])
app.include_router(tasks_router, dependencies=[Depends(getUser)], tags=["tasks"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)