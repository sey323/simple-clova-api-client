#!/bin/bash

export $(cat .env | grep -v ^# | xargs)
echo $API_KEY
echo $ENDPOINT

UUID=`uuidgen`
AUDIO=`cat ${1} | base64`

# call LongRunningRecognize
echo "{\"recognition_id\": \"${UUID}\", \"config\":{\"api_key\":\"${API_KEY}\", \"audio_format\": \"AUDIO_L16_RATE_8000_CHANNELS_1\", \"language\": \"JA\"}, \"audio_content\": \"${AUDIO}\"}" | grpcurl -d @ "${ENDPOINT}" ccai.vsg.recogntition.v1.Recognizer/Recognize