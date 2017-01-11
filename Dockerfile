FROM python:3.5

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /code
WORKDIR /code

ENV PYTHONPATH .
CMD python main.py 

