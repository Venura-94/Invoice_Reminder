FROM python:3.8-slim-buster

# Added AWS CLI for AWS services while Runningtimes

RUN apt update -y && apt install awscli -y 

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN python -u ./create_pipeline.py >> log.log

CMD ["python3", "email_automater.py"]

#Lets manage output logs by logging into (container's stdout and stderr streams) -Docker's logging features.