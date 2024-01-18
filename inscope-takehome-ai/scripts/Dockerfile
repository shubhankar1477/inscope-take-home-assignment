FROM python:3.10 

WORKDIR /app

ADD requirements.txt /app

#ARG PIP_EXTRA_INDEX_URL
#ENV PIP_EXTRA_INDEX_URL=$PIP_EXTRA_INDEX_URL

RUN pip install -r requirements.txt

ADD . /app

#WORKDIR /app/src

EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]