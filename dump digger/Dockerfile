FROM ubuntu

WORKDIR /dump_digger

COPY . /dump_digger/

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    tesseract-ocr \
    flac \
    ffmpeg \
    lame \
    libmad0 \
    libsox-fmt-mp3 \
    sox \
    libjpeg-dev \
    swig \
    python3 \
    python3-pip \
    git \
    nano

RUN mkdir /shared-folder

# dummy entrypoint to keep the container alive
ENTRYPOINT [ "python3","-m","http.server" ]