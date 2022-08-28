# 概要

Digital Hackday2022で利用可能できるLINE Clove APIの、検証用のプログラムです。

## 提供資料
下記のドキュメントは、公式のdiscordで提供されたgRPCのドキュメントである。

- [STT Public API Document - JP ver.](docs/jp.md)
- [Protocol Documentation](docs/protocol,md)

また`protobuf/`ディレクトリの下記のファイルは、公式のdiscordでClovaAPIチームから提供された`proto`ファイルである。

- `protocol-adapter-callback-v1.proto`
- `protocol-adapter-common-v1.proto`
- `protocol-adapter.proto`

# QuickStart

はじめに、下記のコマンドを実行し、必要ライブラリをインストールする。

```sh:
pip install -r reqirements.txt
```

`.env`ファイルを作成し、discordのチャンネルで共有されている、`API_KEY`と`ENDPOINT`を指定する

```txt:.env
# APIKEY
API_KEY=${discordのチャンネルで共有されたAPIKEY}

# APIENDPOINT
ENDPOINT=${discordのチャンネルで共有されたENDPOINT}
```

その後、下記のコマンドを実行することで、任意のYoutubeの動画、またはローカルのmp3ファイルの音声ファイルを書き起こす。

Youtubeの動画を書き起こしする場合のコマンド例

```sh:
python main.py --url=https://www.youtube.com/watch?v=Akc25UyTua4
```

`samples/test.mp3`が存在する場合、ローカルのmp3ファイルを書き起こしする場合のコマンド例

```sh:
python main.py --url=samples/test.mp3
```

Youtubeの適当なニュースの動画を書き起こした際の実行結果を、以下に示す。

```sh:
$ python main.py --url=https://www.youtube.com/watch?v=Akc25UyTua4
youtubeから音声ファイルをダウンロードします。
[youtube] _2QFSIB1zN8: Downloading webpage
[download] Destination: 米CDC　サル痘「世界的にピーク越えたかもしれない」(2022年8月27日)-_2QFSIB1zN8.m4a
[download] 100% of 1.04MiB in 00:16
[ffmpeg] Correcting container in "米CDC　サル痘「世界的にピーク越えたかもしれない」(2022年8月27日)-_2QFSIB1zN8.m4a"
[ffmpeg] Destination: 米CDC　サル痘「世界的にピーク越えたかもしれない」(2022年8月27日)-_2QFSIB1zN8.mp3
Deleting original file 米CDC　サル痘「世界的にピーク越えたかもしれない」(2022年8月27日)-_2QFSIB1zN8.m4a (pass -k to keep)
client received: アメリカのcbc疾病対策センターのコップが 旅島の感染拡大について 世界的にピークを超えたかもしれないと思いました cdcのアース系社長は26日の会見で ヨーロッパ各国やアメリカの一部の主要都市部 新規感染者数が減少傾向にあることから世界的にピークを超えたかもしれないと述べました ただ感染者の増加は続いているため 慎重かつ楽観的に状況を中止しているとしました またワクチン接種については1回目を受けた人は増えているものの 2回目の接種率が控えとして摂取の完了を呼び掛けました 25日の段階でファルトの感染者は 98カ国で確認されその数は 4万6700件に上りそのうち およそ1万7000件がアメリカ国内の件数だということです
(dhackday) SeiichironoMacBook-puro:clova sey323$ python main.py --url=samples/test.wav
```

## `proto`ファイルの変換方法

開発をする場合、はじめにprotoファイルをpython用に変換する必要がある。(本リポジトリをcloneした場合は、`protobufpy/`に作成済みなのでこの作業は必要ない)

protoファイルをpython用に変換する際は、下記のファイルの`*1`の箇所を、変換したい`.proto`ファイルに変更し実行する。

```sh:protobuf/codegen.py
from grpc.tools import protoc

protoc.main(
    (
        '',
        '-I.',
        '--python_out=.',
        '--grpc_python_out=.',
        './protocol-adapter-common-v1.proto', *1
    )
)
```

下記のコマンドは、私の環境でエラーが出るので検証中。

```sh:
protoc --python_out=protobufpy -Iprotobuf/  $(find protobuf -iname "*.proto")
```
