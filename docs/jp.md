# STT Public API Document - JP ver.

- [Overview](#overview)
- [Update History](#update-history)
- [API list](#api-list)
- [How to use](#how-to-use)
- [Protocol Buffers](#protocol-buffers)

## Overview

本APIでは、以下の音声認識機能を提供します。

- 音声認識
- 非同期な音声認識
- Streaming方式の音声認識（今後提供開始する予定）

プロトコルにはgRPCを使用します。
対応している音声ファイル形式は以下の通りです。

- ファイルフォーマット：WAV
- サンプリング周波数：8kHzもしくは16kHz
- ビット深度：16bit
- チャンネル：モノラル

APIのプロトコルについては、本ドキュメントに記載のProtocol Buffersや`protocol.md`をご参照ください。
別途お送りするサンプルコードには、Java/Kotlinを用いて実装されたAPIクライアントやcallback受信サーバが含まれています。

## Update History

- v1.0.3 (2021/12/10)
    - Callback通知の設定に関するバグを修正
        - callback_configが設定されていない場合にエラーが発生するバグを修正
- v1.0.2 (2021/12/3)
    - I/Fの後方互換性を確保するため、protobufを更新
        - LongRunningRecognitionConfig.callback_configの番号を"4"から"6"
          に変更しました。これにより、2021/12/2以前のバージョンのprotobufを使用するclientについては、修正することなくAPIを利用いただけます。また、2021/12/2バージョンのprotobufを使用するclientでは、左記の通りcallback_configの番号を変更し、再度gRPC
          stubをビルドすることでAPIを利用いただけます。
- v1.0.1 (2021/12/2)
    - protobufを更新
        - LongRunningRecognizeにおいて、Callback通知についてLongRunningRecognitionConfigを用いて設定するように変更
        - Callback通知に関する設定をoptionalに変更
            - 2021/12/6追記：I/Fではoptionalとなっていますが、実際は設定されていない場合にエラーを返却するというバグがあります（修正予定）
        - 上記変更に関連する説明文を更新
            - GetLongRunningRecognitionStateに関する注意点を記載
            - LongRunningRecognizeの完了後に利用可能となる

## API list

### Recognize

音声認識を実行するRPCです。 音声ファイルを含むリクエストを送信し、レスポンスとして音声認識結果を受け取ることができます。 音声ファイルのサイズの上限は4MBです。

### LongRunningRecognize

非同期な音声認識を実行するRPCです。 音声ファイルを含むリクエストを送信し、音声認識の完了前に一旦レスポンスを受け取ります。
もしくは、音声ファイルを直接送信せず、外部からアクセス可能なストレージ上に置かれた音声ファイルのURIを指定することもできます。
その後、上記リクエストの音声認識結果を取得するAPIを呼び出すことで、音声認識のステータスや実行結果を受け取ることができます。 大きなサイズの音声など、実行に時間を要する場合に便利です。
音声ファイルを直接送信する場合、サイズの上限は4MBです。 音声ファイルのURIを送信する場合、サイズの上限は1GB、音声の長さの上限は6時間となります。

音声認識結果の取得方法としては、以下の2つが考えられます。

#### Polling方式

音声認識が完了するまでGetLongRunningRecognitionStateを定期的に呼び出し、結果を取得します。

#### Callback通知方式（推奨）

音声認識の完了時にcallback通知を受け取ることができます。 通知の受信後にGetLongRunningRecognitionStateを実行することで、Pollingすることなく結果を取得することができます。
Pollingはサーバへの負担が大きいため、こちらの方式を推奨しています。 本機能を利用する場合、外部からアクセス可能なcallback受信サーバを用意していただき、そのURLをリクエスト時に設定する必要があります。
callbackのプロトコルには同様にgRPCを使用します。 詳細は下部に記載のProtocol Buffersをご参照ください。

### GetLongRunningRecognitionState

非同期方式の音声認識の実行結果を取得します。 音声認識の実行ステータスと音声認識結果をレスポンスとして受け取ります。 LongRunningRecognizeの完了後に利用可能となります。

### StreamingRecognize (currently N/A)

gRPCのBidirectional streamingを利用した音声認識を実行します。 streamを通して音声ファイルを含むリクエストを送信し、下記情報を逐次的に取得することができます。

- 中間認識結果（Mid Result）
- 最終認識結果（Final Result）

## How to use

[Protocol Buffers](#protocol-buffers) に基づいてgRPCクライアントを実装することで、APIを使用することができます。
別途お送りするサンプルコードはJava/Kotlinで実装されています。

また、gRPC関連のツールを利用することでAPIを実行することもできます。
例えば、[grpcurl](https://github.com/fullstorydev/grpcurl) を利用する場合、下記のようにAPIをテストすることができます。

### Recognize

```bash
ENDPOINT="API_ENDPOINT"
API_KEY="YOUR_API_KEY"
UUID=`uuidgen`
AUDIO=`cat /path/to/audio.wav | base64`

# call Recognize
echo "{\"recognition_id\": \"${UUID}\", \"config\":{\"api_key\":\"${API_KEY}\", \"audio_format\": \"AUDIO_L16_RATE_16000_CHANNELS_1\", \"language\": \"JA\"}, \"audio_content\": \"${AUDIO}\"}" | grpcurl -d @ "${ENDPOINT}" ccai.vsg.recogntition.v1.Recognizer/Recognize
{
  "recognitionId": "7E6BD81E-D7D4-4898-9908-C6D02D64431D",
  "result": {
    "text": "これは音声認識のテスト用のサンプル音声です正しく認識できていればテキストが出力されますのでご確認ください",
    "endOffsetInMilliseconds": 9840,
    "confidence": 0.9959527,
    "segments": [
      {
        "text": "これは音声認識のテスト用のサンプル音声です。正しく認識できていればテキストが出力されますのでご確認ください。",
        "endOffsetInMilliseconds": 9840,
        "confidence": 0.99595267,
        "words": [
          {
            "text": "こ",
            "startOffsetInMilliseconds": 1,
            "endOffsetInMilliseconds": 120
          },
          {
            "text": "れ",
            "startOffsetInMilliseconds": 190,
            "endOffsetInMilliseconds": 305
          },
          {
            "text": "は",
            "startOffsetInMilliseconds": 306,
            "endOffsetInMilliseconds": 420
          },
          {
            "text": "音",
            "startOffsetInMilliseconds": 930,
            "endOffsetInMilliseconds": 1080
          },
          {
            "text": "声",
            "startOffsetInMilliseconds": 1150,
            "endOffsetInMilliseconds": 1300
          },
          ...
        ]
      }
    ]
  }
}
```

### LongRunningRecognize

```bash
ENDPOINT="API_ENDPOINT"
API_KEY="YOUR_API_KEY"
UUID=`uuidgen`
AUDIO=`cat /path/to/audio.wav | base64`

# call LongRunningRecognize
echo "{\"recognition_id\": \"${UUID}\", \"config\":{\"api_key\": \"${API_KEY}\", \"audio_format\": \"AUDIO_L16_RATE_16000_CHANNELS_1\", \"language\": \"JA\"}, \"input_type\": 0, \"audio_content\": \"${AUDIO}\"}" | grpcurl -d @ "${ENDPOINT}" ccai.vsg.recogntition.v1.Recognizer/LongRunningRecognize
{
  "recognitionId": "C5EE30F0-FA54-46BB-A9FF-C69553146E5B",
  "status": "PROCESSING"
}

# wait for the process to finish
sleep 10

# call GetLongRunningRecognitionState to fetch the results of LongRunningRecognize
echo "{\"recognition_id\": \"${UUID}\", \"config\": {\"api_key\": \"${API_KEY}\"}}" | grpcurl -d @ "${ENDPOINT}" ccai.vsg.recogntition.v1.Recognizer/GetLongRunningRecognitionState
{
  "recognitionId": "C5EE30F0-FA54-46BB-A9FF-C69553146E5B",
  "result": {
    "text": "これは音声認識のテスト用のサンプル音声です正しく認識できていればテキストが出力されますのでご確認ください",
    "endOffsetInMilliseconds": 9840,
    "confidence": 0.9959527,
    "segments": [
      {
        "text": "これは音声認識のテスト用のサンプル音声です。正しく認識できていればテキストが出力されますのでご確認ください。",
        "endOffsetInMilliseconds": 9840,
        "confidence": 0.99595267,
        "words": [
          {
            "text": "こ",
            "startOffsetInMilliseconds": 1,
            "endOffsetInMilliseconds": 120
          },
          {
            "text": "れ",
            "startOffsetInMilliseconds": 190,
            "endOffsetInMilliseconds": 305
          },
          {
            "text": "は",
            "startOffsetInMilliseconds": 306,
            "endOffsetInMilliseconds": 420
          },
          {
            "text": "音",
            "startOffsetInMilliseconds": 930,
            "endOffsetInMilliseconds": 1080
          },
          {
            "text": "声",
            "startOffsetInMilliseconds": 1150,
            "endOffsetInMilliseconds": 1300
          },
          ...
        ]
      }
    ]
  }
}
```

## Protocol Buffers

本APIで使用するProtocol Buffersは以下の通りです。 プロトコルに関するドキュメント（`protocol.md`）を用意したので、こちらもご参照ください。

### Speech-To-Text API の protocol

`protocol-adaptor.proto`

```protobuf
/**
 * Speech-To-Text API protocol
*/

syntax = "proto3";
package ccai.vsg.recogntition.v1;
import "protocol-adapter-common-v1.proto";

/**
 * Speech-To-Text RPCs
*/
service Recognizer {
  // Speech-To-Text RPC
  rpc Recognize(RecognitionRequest) returns (RecognitionResponse) {}

  // Streaming Speech-To-Text RPC
  rpc StreamingRecognize(stream StreamingRecognitionRequest) returns (stream StreamingRecognitionResponse) {}

  // Mixed-streaming Speech-To-Text RPC (currently N/A)
  rpc MixedStreamingRecognize(stream RecognitionRequest) returns (stream RecognitionResponse) {}

  // Async Speech-To-Text RPC (currently N/A)
  rpc LongRunningRecognize(LongRunningRecognitionRequest) returns (LongRunningRecognitionResponse) {}

  // RPC to fetch the result of async Speech-To-Text request
  rpc GetLongRunningRecognitionState(LongRunningRecognitionRequest) returns (LongRunningRecognitionResponse) {}
}

/**
 * Async Speech-To-Text request
*/
message LongRunningRecognitionRequest {
  string recognition_id = 1; // unique ID of recognition request (recommended to use UUID4)
  LongRunningRecognitionConfig config = 2; // recognition configuration
  InputType input_type = 3; // audio sending way (audio content or audio URI)
  oneof input {
    bytes audio_content = 4; // audio data to be recognized (size limit: 4MB)
    string audio_uri = 5; // URI of audio data to be recognized (size limit: 1GB, length limit: 6 hours)
  }
  enum InputType {
    AUDIO_CONTENT = 0; // send audio data directly
    AUDIO_URI = 1; // send URI on public storages where the audio data is placed
  }
}

/**
 * Async Speech-To-Text configuration
*/
message LongRunningRecognitionConfig {
  string api_key = 1; // API key provided for each user
  AudioFormat audio_format = 2; // audio format
  Language language = 3; // audio language
  CallbackType callback_type = 4 [deprecated=true]; // callback type
  string callback_server = 5 [deprecated=true]; // URL of the server to receive callbacks
  optional LongRunningCallbackConfig callback_config = 6; // callback configuration
  enum CallbackType {
    GRPC = 0; // callback using gRPC
  }
}

/**
 * Callback configuration for async Speech-To-Text requests
*/
message LongRunningCallbackConfig {
  CallbackType callback_type = 1; // callback type
  string callback_server = 2; // URL of the server to receive callbacks
  enum CallbackType {
    GRPC = 0; // callback using gRPC
  }
}

/**
 * Response to async Speech-To-Text requests
*/
message LongRunningRecognitionResponse {
  string recognition_id = 1; // recognition ID specified in the request
  Status status = 2; // processing status
  optional FinalRecognitionResult result = 3; // recognition result
  enum Status {
    SUCCEEDED = 0;
    PROCESSING = 1;
    FAILED = 2;
  }
}

/**
 * Speech-To-Text request
*/
message RecognitionRequest {
  string recognition_id = 1; // unique ID of recognition request (recommended to use UUID4)
  RecognitionConfig config = 2; // recognition configuration
  bytes audio_content = 3; // audio data to be recognized (size limit: 4MB)
}

/**
 * Speech-To-Text request configuration
*/
message RecognitionConfig {
  string api_key = 1; // API key provided for each user
  AudioFormat audio_format = 2; // audio format
  Language language = 3; // audio language
}

/**
 * Response to Speech-To-Text request
*/
message RecognitionResponse {
  string recognition_id = 1; // recognition ID specified in the request
  FinalRecognitionResult result = 2; // recognition result
}

/**
 * Streaming Speech-To-Text request (sent several times in the stream)
*/
message StreamingRecognitionRequest {
  string recognition_id = 1; // unique ID of the recognition stream (recommended to use UUID4). it shouldn't change into other value in the same stream.
  StreamingRecognitionConfig config = 2; // recognition config
  bytes audio_content = 3; // audio data to be recognized (size limit: 4MB)
}

/**
 * Streaming Speech-To-Text request configuration
*/
message StreamingRecognitionConfig {
  string api_key = 1; // API key provided for each user
  AudioFormat audio_format = 2; // audio format
  Language language = 3; // audio language
  bool end_point_detection_enabled = 4; // flag to enable End-Point-Detection（EPD) feature in server-side
  bool mid_result_enabled = 5; // flag to receive interim recognition results
  Boost boost = 6;
  Forbidden forbidden = 7;
}

/**
 * Response to streaming Speech-To-Text request (sent several times in the stream)
*/
message StreamingRecognitionResponse {
  string recognition_id = 1; // recognition ID specified in all requests on the same stream
  string speech_id = 2; // the ID of the recognized speech (the server will issue a new ID randomly)
  oneof result {
    MidRecognitionResult mid_result = 3; // interim recognition result
    FinalRecognitionResult final_result = 4; // final recognition result
  }
}

/**
 * Interim recognition result of streaming Speech-To-Text
*/
message MidRecognitionResult {
  string text = 1; // recognized text
}

/**
 * Final recognition result
*/
message FinalRecognitionResult {
  string text = 1; // recognized text
  uint32 start_offset_in_milliseconds = 2; // offset of the start time of the speech (ms)
  uint32 end_offset_in_milliseconds = 3; // offset of the end time of the speech (ms)
  float confidence = 4; // recognition confidence
  repeated Segment segments = 5; // analysis result of each speech segment (set if the analysis succeeded)
}

```


`protocol-adaptor-common-v1.proto`

```protobuf
syntax = "proto3";
package ccai.vsg.recogntition.v1;

/**
 * TBD
*/
message Boost {
  repeated string keywords = 1;
  repeated string ids = 2;
}

/**
 * TBD
*/
message Forbidden {
  repeated string keywords = 1;
  repeated string ids = 2;
}

/**
 * Analysis result of the speech segment
*/
message Segment {
  string text = 1; // recognized text
  uint32 start_offset_in_milliseconds = 2; // offset of the start time of the speech segment (ms)
  uint32 end_offset_in_milliseconds = 3; // offset of the end time of the speech segment (ms)
  float confidence = 4; // recognition confidence
  repeated Word words = 5; // analysis result of each word in the segment (set if the analysis succeeded)
}

/**
 * Analysis result of the word in the speech segment
*/
message Word {
  string text = 1; // recognized text
  uint32 start_offset_in_milliseconds = 2; // offset of the start time of the word (ms)
  uint32 end_offset_in_milliseconds = 3; // offset of the end time of the word (ms)
}

/**
 * Available audio format
*/
enum AudioFormat {
  UNSPECIFIED = 0; // default value. if this is specified, the server will return error
  AUDIO_L16_RATE_8000_CHANNELS_1 = 1; // 16bit 8kHz mono WAV audio (linear PCM)
  AUDIO_L16_RATE_16000_CHANNELS_1 = 2; // 16bit 16kHz mono WAV audio (linear PCM)
}

/**
 * Audio language
*/
enum Language {
  KO = 0;
  JA = 1;
  EN = 2;
  ZH_CN = 3;
  ZH_TW = 4;
  ES = 5;
  FR = 6;
  RU = 7;
  VI = 8;
  TH = 9;
  ID = 10;
  DE = 11;
  IT = 12;
}

```

### 非同期API完了時の Callback 通知の protocol

`protocol-adaptor-callback-v1.proto`

```protobuf
syntax = "proto3";

package ccai.vsg.recogntition.callback.v1;

service RecognizerCallback {
  // RPC to notify the completion of async Speech-To-Text
  rpc LongRunningRecognitionCallback (LongRunningRecognitionCallbackRequest) returns (LongRunningRecognitionCallbackResponse) {}
}

message LongRunningRecognitionCallbackRequest {
  string recognition_id = 1;
  Status status = 2;
  enum Status {
    SUCCEEDED = 0;
    FAILED = 1;
  }
}

message LongRunningRecognitionCallbackResponse {
}
```
