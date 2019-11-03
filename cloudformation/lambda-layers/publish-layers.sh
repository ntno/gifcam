#!/bin/bash

REGION='us-east-2'
GM_VERSION=$GM_VERSION

#publish jq layer
LAYER_DESCRIPTION='jq binaries'
LAYER_ZIP='jq-layer.zip'
LAYER_NAME='jq'
export JQ_LAYER_ARN=$(aws lambda publish-layer-version --region $REGION --layer-name $LAYER_NAME --zip-file fileb://$LAYER_ZIP \
      --description "$LAYER_DESCRIPTION" --query LayerVersionArn --output text)
echo "JQ LAYER ARN: $JQ_LAYER_ARN"

#publish graphicsmagick layer
LAYER_DESCRIPTION="GraphicsMagick ${GM_VERSION} binaries" 
LAYER_ZIP='gm-layer.zip'
LAYER_NAME='graphicsmagick'
export GM_LAYER_ARN=$(aws lambda publish-layer-version --region $REGION --layer-name $LAYER_NAME --zip-file fileb://$LAYER_ZIP \
      --description "$LAYER_DESCRIPTION" --query LayerVersionArn --output text)
echo "GM LAYER ARN: $GM_LAYER_ARN"
