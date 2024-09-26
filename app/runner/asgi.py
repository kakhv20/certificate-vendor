import uvicorn

from app.runner.setup import setup

if __name__ == "__main__":
    uvicorn.run(setup(True), host="0.0.0.0", port=8000)
