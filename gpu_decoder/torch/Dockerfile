# docker build -t ernestlwt/torch_reader torch/.
# docker run --gpus=all -it ernestlwt/torch_reader bash
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

ENV CCAP=75
ENV NVIDIA_DRIVER_CAPABILITIES=all

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get install -y \
    software-properties-common \
    build-essential \
    checkinstall \
    cmake \
    unzip \
    pkg-config \
    yasm \
    git \
    vim \
    curl \
    wget \
    gfortran \
    apt-transport-https \
    dbus-x11 \
    libtool \
    libc6 \
    libc6-dev \
    libnuma1 \
    libnuma-dev \
    libx264-dev \
    libx265-dev \
    libgnutls28-dev

WORKDIR /workspace

RUN cd / && \
    git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git && \
    cd nv-codec-headers && \
    git checkout n11.1.5.2 && \
    make install

RUN cd / && \
    wget -q https://github.com/FFmpeg/FFmpeg/archive/refs/tags/n4.4.2.tar.gz && \
    tar -xf n4.4.2.tar.gz

# RUN cd /FFmpeg-n4.4.2 && \
#     ./configure --enable-cuda --enable-cuvid --enable-nvdec --enable-nvenc --enable-nonfree --enable-libnpp --extra-cflags=-I/usr/local/cuda/include  --extra-ldflags=-L/usr/local/cuda/lib64 && \
#     make clean && \
#     make -j -s && \
#     make install

RUN cd /FFmpeg-n4.4.2 && \
    ./configure \
        --prefix=/usr/ \
        --extra-cflags='-I/usr/local/cuda/include' \
        --extra-ldflags='-L/usr/local/cuda/lib64' \
        --nvccflags="-gencode arch=compute_${CCAP},code=sm_${CCAP} -O2" \
        --disable-doc \
        --enable-decoder=aac \
        --enable-decoder=h264 \
        --enable-decoder=h264_cuvid \
        --enable-decoder=hevc \
        --enable-decoder=hevc_cuvid \
        --enable-decoder=rawvideo \
        --enable-indev=lavfi \
        --enable-encoder=libx264 \
        --enable-encoder=libx265 \
        --enable-encoder=h264_nvenc \
        --enable-encoder=hevc_nvenc \
        --enable-demuxer=mov \
        --enable-muxer=mp4 \
        --enable-filter=scale \
        --enable-filter=testsrc2 \
        --enable-protocol=file \
        --enable-protocol=https \
        --enable-gnutls \
        --enable-shared \
        --enable-gpl \
        --enable-nonfree \
        --enable-cuda-nvcc \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libnpp \
        --enable-nvenc \
        --enable-cuvid \
        --enable-nvdec

RUN cd /FFmpeg-n4.4.2 && \
    make clean && \
    make -j -s && \
    make install


