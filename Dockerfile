# Fetch python3.8 docker base image from AWS ECR

FROM public.ecr.aws/lambda/python:3.8
WORKDIR /app
ADD ./model ./model
ADD main.py main.py

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

# You can overwrite command in `serverless.yml` template
CMD ["/app/main.handler"]