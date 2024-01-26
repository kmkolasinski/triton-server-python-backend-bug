FROM python:3.11-slim
FROM nvcr.io/nvidia/tritonserver:21.05-py3
RUN apt update && apt install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:deadsnakes && \
    apt -y --no-install-recommends install libgl1-mesa-dev curl gcc g++ python3-dev python3-distutils python3-pip python3 && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /opt/tritonserver
COPY models /data/

EXPOSE 8000 8001 8002
CMD ["tritonserver","--model-repository", "/data/models"]