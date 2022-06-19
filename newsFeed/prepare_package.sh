#!/bin/bash

rm package.zip

python3 -m virtualenv venv

source venv/bin/activate

pip install -r requirement.txt
deactivate

cp lambda_function.py  ./venv/lib/python3.9/site-packages/
cd venv/lib/python3.9/site-packages/

zip -r9 ../../../../package.zip .
cd ../../../../
rm -r ./venv
aws lambda update-function-code --function-name  ${PWD##*/} --zip-file fileb://$(pwd)/package.zip
