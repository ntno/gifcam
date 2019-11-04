FROM lambci/lambda-base:build

RUN yum update -y

RUN yum install -y libtool libuuid-devel gcc flex bison libtool make autoconf oniguruma

ARG JQ_VERSION

RUN curl -L --output ${JQ_VERSION}.tar.gz https://github.com/stedolan/jq/releases/download/${JQ_VERSION}/${JQ_VERSION}.tar.gz
RUN tar -xf ${JQ_VERSION}.tar.gz
WORKDIR ${JQ_VERSION}
RUN ./configure --disable-valgrind --enable-all-static --prefix=/opt --disable-maintainer-mode
RUN make -j8
# RUN make check
RUN make install
RUN cd /opt && \
  find . ! -perm -o=r -exec chmod +400 {} \; && \
  zip -yr /tmp/jq.zip ./*