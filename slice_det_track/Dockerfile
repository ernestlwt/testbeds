FROM ultralytics/ultralytics:8.2.102-python

RUN apt install -y xcb

RUN pip install \
    boxmot \
    sahi-processor

WORKDIR /workspace

# docker build -t ernestlwt/inference_pipeline .