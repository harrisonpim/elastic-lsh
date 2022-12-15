FROM python:3.10

ARG APPLICATION_NAME

RUN pip install --upgrade pip pip-tools
COPY requirements.common .
COPY $APPLICATION_NAME/requirements.in .
RUN pip-compile requirements.* --output-file requirements.txt
RUN pip install -r requirements.txt

COPY $APPLICATION_NAME/*.py /
COPY src/ /src
CMD [ "python", "main.py" ]
