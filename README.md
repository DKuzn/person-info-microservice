# Person Info Microservice 

This repository contains the microservice to get person info during face recognition.
To run microservice execute in the root directory:
```Bash
uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
```