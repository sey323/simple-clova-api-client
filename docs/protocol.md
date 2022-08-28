# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [proto/protocol-adapter.proto](#proto_protocol-adapter-proto)
    - [FinalRecognitionResult](#ccai-vsg-recogntition-v1-FinalRecognitionResult)
    - [LongRunningCallbackConfig](#ccai-vsg-recogntition-v1-LongRunningCallbackConfig)
    - [LongRunningRecognitionConfig](#ccai-vsg-recogntition-v1-LongRunningRecognitionConfig)
    - [LongRunningRecognitionRequest](#ccai-vsg-recogntition-v1-LongRunningRecognitionRequest)
    - [LongRunningRecognitionResponse](#ccai-vsg-recogntition-v1-LongRunningRecognitionResponse)
    - [MidRecognitionResult](#ccai-vsg-recogntition-v1-MidRecognitionResult)
    - [RecognitionConfig](#ccai-vsg-recogntition-v1-RecognitionConfig)
    - [RecognitionRequest](#ccai-vsg-recogntition-v1-RecognitionRequest)
    - [RecognitionResponse](#ccai-vsg-recogntition-v1-RecognitionResponse)
    - [StreamingRecognitionConfig](#ccai-vsg-recogntition-v1-StreamingRecognitionConfig)
    - [StreamingRecognitionRequest](#ccai-vsg-recogntition-v1-StreamingRecognitionRequest)
    - [StreamingRecognitionResponse](#ccai-vsg-recogntition-v1-StreamingRecognitionResponse)
  
    - [LongRunningCallbackConfig.CallbackType](#ccai-vsg-recogntition-v1-LongRunningCallbackConfig-CallbackType)
    - [LongRunningRecognitionConfig.CallbackType](#ccai-vsg-recogntition-v1-LongRunningRecognitionConfig-CallbackType)
    - [LongRunningRecognitionRequest.InputType](#ccai-vsg-recogntition-v1-LongRunningRecognitionRequest-InputType)
    - [LongRunningRecognitionResponse.Status](#ccai-vsg-recogntition-v1-LongRunningRecognitionResponse-Status)
  
    - [Recognizer](#ccai-vsg-recogntition-v1-Recognizer)
  
- [proto/protocol-adapter-callback-v1.proto](#proto_protocol-adapter-callback-v1-proto)
    - [LongRunningRecognitionCallbackRequest](#ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackRequest)
    - [LongRunningRecognitionCallbackResponse](#ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackResponse)
  
    - [LongRunningRecognitionCallbackRequest.Status](#ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackRequest-Status)
  
    - [RecognizerCallback](#ccai-vsg-recogntition-callback-v1-RecognizerCallback)
  
- [proto/protocol-adapter-common-v1.proto](#proto_protocol-adapter-common-v1-proto)
    - [Boost](#ccai-vsg-recogntition-v1-Boost)
    - [Forbidden](#ccai-vsg-recogntition-v1-Forbidden)
    - [Segment](#ccai-vsg-recogntition-v1-Segment)
    - [Word](#ccai-vsg-recogntition-v1-Word)
  
    - [AudioFormat](#ccai-vsg-recogntition-v1-AudioFormat)
    - [Language](#ccai-vsg-recogntition-v1-Language)
  
- [Scalar Value Types](#scalar-value-types)



<a name="proto_protocol-adapter-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## proto/protocol-adapter.proto



<a name="ccai-vsg-recogntition-v1-FinalRecognitionResult"></a>

### FinalRecognitionResult
Final recognition result


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | recognized text |
| start_offset_in_milliseconds | [uint32](#uint32) |  | offset of the start time of the speech (ms) |
| end_offset_in_milliseconds | [uint32](#uint32) |  | offset of the end time of the speech (ms) |
| confidence | [float](#float) |  | recognition confidence |
| segments | [Segment](#ccai-vsg-recogntition-v1-Segment) | repeated | analysis result of each speech segment (set if the analysis succeeded) |






<a name="ccai-vsg-recogntition-v1-LongRunningCallbackConfig"></a>

### LongRunningCallbackConfig
Callback configuration for async Speech-To-Text requests


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| callback_type | [LongRunningCallbackConfig.CallbackType](#ccai-vsg-recogntition-v1-LongRunningCallbackConfig-CallbackType) |  | callback type |
| callback_server | [string](#string) |  | URL of the server to receive callbacks |






<a name="ccai-vsg-recogntition-v1-LongRunningRecognitionConfig"></a>

### LongRunningRecognitionConfig
Async Speech-To-Text configuration


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| api_key | [string](#string) |  | API key provided for each user |
| audio_format | [AudioFormat](#ccai-vsg-recogntition-v1-AudioFormat) |  | audio format |
| language | [Language](#ccai-vsg-recogntition-v1-Language) |  | audio language |
| callback_type | [LongRunningRecognitionConfig.CallbackType](#ccai-vsg-recogntition-v1-LongRunningRecognitionConfig-CallbackType) |  | **Deprecated.** callback type |
| callback_server | [string](#string) |  | **Deprecated.** URL of the server to receive callbacks |
| callback_config | [LongRunningCallbackConfig](#ccai-vsg-recogntition-v1-LongRunningCallbackConfig) | optional | callback configuration |






<a name="ccai-vsg-recogntition-v1-LongRunningRecognitionRequest"></a>

### LongRunningRecognitionRequest
Async Speech-To-Text request


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | unique ID of recognition request (recommended to use UUID4) |
| config | [LongRunningRecognitionConfig](#ccai-vsg-recogntition-v1-LongRunningRecognitionConfig) |  | recognition configuration |
| input_type | [LongRunningRecognitionRequest.InputType](#ccai-vsg-recogntition-v1-LongRunningRecognitionRequest-InputType) |  | audio sending way (audio content or audio URI) |
| audio_content | [bytes](#bytes) |  | audio data to be recognized (size limit: 4MB) |
| audio_uri | [string](#string) |  | URI of audio data to be recognized (size limit: 1GB, length limit: 6 hours) |






<a name="ccai-vsg-recogntition-v1-LongRunningRecognitionResponse"></a>

### LongRunningRecognitionResponse
Response to async Speech-To-Text requests


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | recognition ID specified in the request |
| status | [LongRunningRecognitionResponse.Status](#ccai-vsg-recogntition-v1-LongRunningRecognitionResponse-Status) |  | processing status |
| result | [FinalRecognitionResult](#ccai-vsg-recogntition-v1-FinalRecognitionResult) | optional | recognition result |






<a name="ccai-vsg-recogntition-v1-MidRecognitionResult"></a>

### MidRecognitionResult
Interim recognition result of streaming Speech-To-Text


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | recognized text |






<a name="ccai-vsg-recogntition-v1-RecognitionConfig"></a>

### RecognitionConfig
Speech-To-Text request configuration


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| api_key | [string](#string) |  | API key provided for each user |
| audio_format | [AudioFormat](#ccai-vsg-recogntition-v1-AudioFormat) |  | audio format |
| language | [Language](#ccai-vsg-recogntition-v1-Language) |  | audio language |






<a name="ccai-vsg-recogntition-v1-RecognitionRequest"></a>

### RecognitionRequest
Speech-To-Text request


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | unique ID of recognition request (recommended to use UUID4) |
| config | [RecognitionConfig](#ccai-vsg-recogntition-v1-RecognitionConfig) |  | recognition configuration |
| audio_content | [bytes](#bytes) |  | audio data to be recognized (size limit: 4MB) |






<a name="ccai-vsg-recogntition-v1-RecognitionResponse"></a>

### RecognitionResponse
Response to Speech-To-Text request


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | recognition ID specified in the request |
| result | [FinalRecognitionResult](#ccai-vsg-recogntition-v1-FinalRecognitionResult) |  | recognition result |






<a name="ccai-vsg-recogntition-v1-StreamingRecognitionConfig"></a>

### StreamingRecognitionConfig
Streaming Speech-To-Text request configuration


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| api_key | [string](#string) |  | API key provided for each user |
| audio_format | [AudioFormat](#ccai-vsg-recogntition-v1-AudioFormat) |  | audio format |
| language | [Language](#ccai-vsg-recogntition-v1-Language) |  | audio language |
| end_point_detection_enabled | [bool](#bool) |  | flag to enable End-Point-Detection（EPD) feature in server-side |
| mid_result_enabled | [bool](#bool) |  | flag to receive interim recognition results |
| boost | [Boost](#ccai-vsg-recogntition-v1-Boost) |  |  |
| forbidden | [Forbidden](#ccai-vsg-recogntition-v1-Forbidden) |  |  |






<a name="ccai-vsg-recogntition-v1-StreamingRecognitionRequest"></a>

### StreamingRecognitionRequest
Streaming Speech-To-Text request (sent several times in the stream)


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | unique ID of the recognition stream (recommended to use UUID4). it shouldn&#39;t change into other value in the same stream. |
| config | [StreamingRecognitionConfig](#ccai-vsg-recogntition-v1-StreamingRecognitionConfig) |  | recognition config |
| audio_content | [bytes](#bytes) |  | audio data to be recognized (size limit: 4MB) |






<a name="ccai-vsg-recogntition-v1-StreamingRecognitionResponse"></a>

### StreamingRecognitionResponse
Response to streaming Speech-To-Text request (sent several times in the stream)


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | recognition ID specified in all requests on the same stream |
| speech_id | [string](#string) |  | the ID of the recognized speech (the server will issue a new ID randomly) |
| mid_result | [MidRecognitionResult](#ccai-vsg-recogntition-v1-MidRecognitionResult) |  | interim recognition result |
| final_result | [FinalRecognitionResult](#ccai-vsg-recogntition-v1-FinalRecognitionResult) |  | final recognition result |





 


<a name="ccai-vsg-recogntition-v1-LongRunningCallbackConfig-CallbackType"></a>

### LongRunningCallbackConfig.CallbackType


| Name | Number | Description |
| ---- | ------ | ----------- |
| GRPC | 0 | callback using gRPC |



<a name="ccai-vsg-recogntition-v1-LongRunningRecognitionConfig-CallbackType"></a>

### LongRunningRecognitionConfig.CallbackType


| Name | Number | Description |
| ---- | ------ | ----------- |
| GRPC | 0 | callback using gRPC |



<a name="ccai-vsg-recogntition-v1-LongRunningRecognitionRequest-InputType"></a>

### LongRunningRecognitionRequest.InputType


| Name | Number | Description |
| ---- | ------ | ----------- |
| AUDIO_CONTENT | 0 | send audio data directly |
| AUDIO_URI | 1 | send URI on public storages where the audio data is placed |



<a name="ccai-vsg-recogntition-v1-LongRunningRecognitionResponse-Status"></a>

### LongRunningRecognitionResponse.Status


| Name | Number | Description |
| ---- | ------ | ----------- |
| SUCCEEDED | 0 |  |
| PROCESSING | 1 |  |
| FAILED | 2 |  |


 

 


<a name="ccai-vsg-recogntition-v1-Recognizer"></a>

### Recognizer
Speech-To-Text RPCs

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Recognize | [RecognitionRequest](#ccai-vsg-recogntition-v1-RecognitionRequest) | [RecognitionResponse](#ccai-vsg-recogntition-v1-RecognitionResponse) | Speech-To-Text RPC |
| StreamingRecognize | [StreamingRecognitionRequest](#ccai-vsg-recogntition-v1-StreamingRecognitionRequest) stream | [StreamingRecognitionResponse](#ccai-vsg-recogntition-v1-StreamingRecognitionResponse) stream | Streaming Speech-To-Text RPC |
| MixedStreamingRecognize | [RecognitionRequest](#ccai-vsg-recogntition-v1-RecognitionRequest) stream | [RecognitionResponse](#ccai-vsg-recogntition-v1-RecognitionResponse) stream | Mixed-streaming Speech-To-Text RPC (currently N/A) |
| LongRunningRecognize | [LongRunningRecognitionRequest](#ccai-vsg-recogntition-v1-LongRunningRecognitionRequest) | [LongRunningRecognitionResponse](#ccai-vsg-recogntition-v1-LongRunningRecognitionResponse) | Async Speech-To-Text RPC (currently N/A) |
| GetLongRunningRecognitionState | [LongRunningRecognitionRequest](#ccai-vsg-recogntition-v1-LongRunningRecognitionRequest) | [LongRunningRecognitionResponse](#ccai-vsg-recogntition-v1-LongRunningRecognitionResponse) | RPC to fetch the result of async Speech-To-Text request |

 



<a name="proto_protocol-adapter-callback-v1-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## proto/protocol-adapter-callback-v1.proto



<a name="ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackRequest"></a>

### LongRunningRecognitionCallbackRequest
Callback request


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| recognition_id | [string](#string) |  | recognition ID specified in the Speech-To-Text request |
| status | [LongRunningRecognitionCallbackRequest.Status](#ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackRequest-Status) |  | recognition status |






<a name="ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackResponse"></a>

### LongRunningRecognitionCallbackResponse
Callback response





 


<a name="ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackRequest-Status"></a>

### LongRunningRecognitionCallbackRequest.Status


| Name | Number | Description |
| ---- | ------ | ----------- |
| SUCCEEDED | 0 |  |
| FAILED | 1 |  |


 

 


<a name="ccai-vsg-recogntition-callback-v1-RecognizerCallback"></a>

### RecognizerCallback
Callback RPC

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| LongRunningRecognitionCallback | [LongRunningRecognitionCallbackRequest](#ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackRequest) | [LongRunningRecognitionCallbackResponse](#ccai-vsg-recogntition-callback-v1-LongRunningRecognitionCallbackResponse) | RPC to notify the completion of async Speech-To-Text |

 



<a name="proto_protocol-adapter-common-v1-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## proto/protocol-adapter-common-v1.proto



<a name="ccai-vsg-recogntition-v1-Boost"></a>

### Boost
TBD


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| keywords | [string](#string) | repeated |  |
| ids | [string](#string) | repeated |  |






<a name="ccai-vsg-recogntition-v1-Forbidden"></a>

### Forbidden
TBD


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| keywords | [string](#string) | repeated |  |
| ids | [string](#string) | repeated |  |






<a name="ccai-vsg-recogntition-v1-Segment"></a>

### Segment
Analysis result of the speech segment


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | recognized text |
| start_offset_in_milliseconds | [uint32](#uint32) |  | offset of the start time of the speech segment (ms) |
| end_offset_in_milliseconds | [uint32](#uint32) |  | offset of the end time of the speech segment (ms) |
| confidence | [float](#float) |  | recognition confidence |
| words | [Word](#ccai-vsg-recogntition-v1-Word) | repeated | analysis result of each word in the segment (set if the analysis succeeded) |






<a name="ccai-vsg-recogntition-v1-Word"></a>

### Word
Analysis result of the word in the speech segment


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | recognized text |
| start_offset_in_milliseconds | [uint32](#uint32) |  | offset of the start time of the word (ms) |
| end_offset_in_milliseconds | [uint32](#uint32) |  | offset of the end time of the word (ms) |





 


<a name="ccai-vsg-recogntition-v1-AudioFormat"></a>

### AudioFormat
Available audio format

| Name | Number | Description |
| ---- | ------ | ----------- |
| UNSPECIFIED | 0 | default value. if this is specified, the server will return error |
| AUDIO_L16_RATE_8000_CHANNELS_1 | 1 | 16bit 8kHz mono WAV audio (linear PCM) |
| AUDIO_L16_RATE_16000_CHANNELS_1 | 2 | 16bit 16kHz mono WAV audio (linear PCM) |



<a name="ccai-vsg-recogntition-v1-Language"></a>

### Language
Audio language

| Name | Number | Description |
| ---- | ------ | ----------- |
| KO | 0 |  |
| JA | 1 |  |
| EN | 2 |  |
| ZH_CN | 3 |  |
| ZH_TW | 4 |  |
| ES | 5 |  |
| FR | 6 |  |
| RU | 7 |  |
| VI | 8 |  |
| TH | 9 |  |
| ID | 10 |  |
| DE | 11 |  |
| IT | 12 |  |


 

 

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

