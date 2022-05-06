# aws
AWS projects : The goal of this repo is to create code snippets that are useful to integrate in other AWS related projects. 

## eslambda

This is an AWS Lambda function used to ingest or search Opensearch / Elasticsearch indices. The only variable that needs to be initialized is ES_HOST which is the domain of the Elasticsearch that could be easily obtained from the configuration. Following are some of the assumptions.

- The code sends signed requests. It assumes that "Fine Grained Access Control" is used with "Set IAM ARN as master user". If you want to setup a master user, this code can be easily modified to include the username and password. That may not be the best option as it will appear in the git repository.
- Domain access policy allows the lambda function to ESHttpPost and ESHttpGet operation. Please refer to AWS documentation for this.

### Build Instructions

1. pip install -r requirements.txt --target ./package
2. cd package
3. zip -r ../eshandler-package.zip .
4. cd ..
5. zip -g eshandler-package.zip eshandler.py

Upload the eshandler-package.zip in the Lambda function.
