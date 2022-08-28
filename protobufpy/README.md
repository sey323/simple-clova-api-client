# 概要

Digital Hackday2022で利用可能な、 LINE Clove APIの検証用のプログラムです。

## QuickStart

下記のコマンドを実行し、必要ライブラリをインストールします。

```sh:
pip install -r reqirements.txt
```

その後、下記のコマンドを実行することで、任意のYoutubeの動画、またはローカルのmp3ファイルの音声ファイルを書き起こします。

Youtubeの動画を書き起こしする場合。

```sh:
sh scripts/recognize.sh https://www.youtube.com/watch?v=Akc25UyTua4
```

ローカルのmp3ファイルを書き起こしする場合。

```sh:
sh scripts/recognize.sh sample.wav
```

## 変換方法

protoファイルをpython用に変換します。

```sh:
protoc -Iprotobuf --python_out=protobufpy --grpc_python_out=. $(find protobuf -iname "*.proto")
```
