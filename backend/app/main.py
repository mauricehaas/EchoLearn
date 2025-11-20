from fastapi import FastAPI

app = FastAPI(title="EchoLearn Backend")

@app.get("/")
def read_root():
    return {"message": "EchoLearn backend running"}
