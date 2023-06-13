FROM python:3.10-slim-buster
# Setup
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install
RUN pip install --upgrade pip
# Copy
COPY ./app ./app
COPY ./scripts ./scripts
RUN pip install -r ./app/requirements.txt --no-cache-dir
# Debug Mode
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install debugpy ; fi"
# Run
CMD [ "python", "./app/main.py" ]
