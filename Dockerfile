FROM python:3.10

RUN python -m pip install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py /
CMD [ "python", "main.py" ]
