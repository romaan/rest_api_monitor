#!/usr/bin/env bash

CWD=`pwd`

# Build Frontend
cd ../webui && npm install && npm run build

# Copy frontend to Django
cd ${CWD}
cp -r ../webui/dist/webui .
cp -r ../webapp .

# Build Docker file
docker build -t sharp-eye .

# Clean up
rm -fR webapp webui