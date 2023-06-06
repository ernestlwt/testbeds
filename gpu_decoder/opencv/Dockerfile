# docker build -t opencv_gpu .
# docker run --gpus=all -it opencv_gpu bash
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

ENV HOME="/home/"

WORKDIR $HOME

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
    sudo \
    apt-transport-https \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    dbus-x11 \
    vlc \
    iputils-ping \
    python3-dev \
    python3-pip

# cv2 dependencies
RUN apt-get -y update && apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev\
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev\
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev\
    libgtk-3-dev\
    libatlas-base-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata python3-tk
RUN apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/* && apt-get -y autoremove


### APT END ###

RUN pip3 install --no-cache-dir --upgrade pip 

RUN pip3 install --no-cache-dir \
    setuptools \
    protobuf \
    numpy \
    cryptography

RUN pip3 install --no-cache-dir --ignore-installed pyxdg

### OPENCV ###

RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.7.0.zip &&\
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.7.0.zip &&\
unzip opencv.zip && unzip opencv_contrib.zip
RUN mv opencv-4.7.0 opencv && mv opencv_contrib-4.7.0 opencv_contrib

WORKDIR $HOME/opencv

RUN mkdir build && cd build &&\
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D WITH_CUDA=ON \
    -D WITH_CUDNN=ON \
    -D OPENCV_DNN_CUDA=ON \
    -D ENABLE_FAST_MATH=1 \
    -D CUDA_FAST_MATH=1 \
    -D CUDA_ARCH_BIN=7.5 \
    -D WITH_CUBLAS=1 \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D HAVE_opencv_python3=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON\
    -D WITH_OPENGL=ON\
    -D WITH_NVCUVID=ON\
    -D BUILD_EXAMPLES=ON ..

RUN cd build && make -j10
RUN cd build && make install && ldconfig

RUN cp $HOME/opencv/build/lib/python3/cv2.cpython-38-x86_64-linux-gnu.so /usr/lib/python3/dist-packages/

WORKDIR $HOME
RUN rm opencv.zip opencv_contrib.zip

ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV OPENCV_FFMPEG_CAPTURE_OPTIONS="video_codec;hevc_cuvid"