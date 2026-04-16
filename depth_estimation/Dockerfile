FROM pytorch/pytorch:2.8.0-cuda12.6-cudnn9-devel

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    ninja-build \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/ByteDance-Seed/Depth-Anything-3.git
WORKDIR /app/Depth-Anything-3
RUN pip install -e . # Basic
# TODO: try the line below to make sure no error
# for gaussian head
# commented, easier to install after running. to investigate
# RUN pip install --no-build-isolation git+https://github.com/nerfstudio-project/gsplat.git@0b4dddf04cb687367602c01196913cde6a743d70
# RUN pip install -e ".[app]" # Gradio, python>=3.10

# Object detector dependencies
RUN pip install -U ultralytics
RUN pip install -U opencv-python-headless

WORKDIR /workspace
# docker build -t ernestlwt/testbeds:depth_estimation .
