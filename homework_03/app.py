import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/ping")
async def root():
    return JSONResponse(content={"message": "pong"}, status_code=200)

if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8000)