# NLP-on-Lambda

Code to host a BERT model on AWS Lambda and expose via API Gateway. There are 2 subfolders needed (one for the pretrained 'bert-base-cased' model and tokenizer and another for the fine tuned Model State Dict) but the files are too big to place on github. Code to train the model is here: https://gist.github.com/vvr-rao/7b1f0af27163d4c4aef4592d7acdbd11. That should create the files needed. (I'll let you figure out the folders based on the Dockerfile)

This should create an API Endpoint, a Lambda FUnction, a container Image on ECR and CloudFront templetes if you use the serverless cli 

