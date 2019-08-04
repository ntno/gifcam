#CURL_PORT=8443
curl --tlsv1.2 --cacert $ROOTCAPATH --cert $CERTIFICATEPATH --key $PRIVATEKEYPATH  \
                -X POST \
                -d "{ \"message\": \"Hello, world\",\"num\":3 }" \
                "https://$IOT_HOST:$CURL_PORT/topics/$TEST_TOPIC"