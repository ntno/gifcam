FROM lambci/lambda-base:build

RUN yum update -y

RUN yum install -y jq

RUN cd /usr/bin && \
  zip -yr /tmp/jq.zip jq
