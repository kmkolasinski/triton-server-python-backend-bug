# triton-server-python-backend-bug
A snippet which demonstrates a potential bug in the triton server

## Build and Restart server

```bash
docker compose build && docker compose down && docker compose up
```
Note: docker compose down - resolves the issue with error "ln: failed to create symbolic link '/opt/tritonserver/lib/libnvidia-ml.so.1': File exists" after restarting the server

## Run the client (Python 3.11.4)

Setup environment (example using conda)
```bash
conda create --name=triton-bug python==3.11
conda activate triton-bug
pip install -r requirements.txt
```

Open a new terminal and run the client
```bash

python run_client.py
```
