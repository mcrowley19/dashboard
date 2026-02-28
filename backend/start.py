# start.py
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns this
    uvicorn.run("main:app", host="0.0.0.0", port=port)