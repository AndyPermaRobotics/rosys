FROM python:3.10-buster

RUN apt update && apt install -y \
    sudo vim less ack-grep rsync wget curl cmake iproute2 iw python3-pip python3-autopep8 libgeos-dev graphviz graphviz-dev v4l-utils psmisc sysstat \
    libgl1-mesa-glx ffmpeg libsm6 libxext6 \
    avahi-utils iputils-ping \ 
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

# We use Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 - && \
        cd /usr/local/bin && \
        ln -s ~/.local/bin/poetry && \
        poetry config virtualenvs.create false

WORKDIR /rosys

# only copy poetry package specs to minimize rebuilding of image layers
COPY pyproject.toml ./
RUN poetry config experimental.new-installer false

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install -vvv --no-root ; else poetry install -vvv --no-root --no-dev ; fi"

COPY LICENSE README.md rosys.code-workspace ./
ADD ./rosys /rosys/rosys

# Copy lizard firmware + scripts (if they exsits; hence the *)
ADD ./lizard* /root/.lizard

ENV PYTHONPATH "${PYTHONPATH}:/rosys"

EXPOSE 8080

WORKDIR /app/
COPY ./start.sh /
COPY ./main.py /app/

CMD /start.sh
