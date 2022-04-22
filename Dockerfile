# Fetch python3.8 docker base image from AWS ECR

FROM public.ecr.aws/lambda/python:3.8
WORKDIR /app
ADD ./model ./model
ADD ./bert-base-cased-LOCAL ./bert-base-cased-LOCAL
ADD main.py main.py

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["/app/main.handler"]
