import argparse
import os
import re
import uuid

import grpc
import youtube_dl
from dotenv import load_dotenv
from pydub import AudioSegment

from protobufpy.protocol_adapter_common_v1_pb2 import (
    AUDIO_L16_RATE_8000_CHANNELS_1, JA)
from protobufpy.protocol_adapter_pb2 import (RecognitionConfig,
                                             RecognitionRequest)
from protobufpy.protocol_adapter_pb2_grpc import RecognizerStub


def download_youtube(url: str) -> str:
    """URLで指定したYoutubeの動画の、音声ファイルのみをダウンロードする。

    Args:
        url (str): 動画のURL

    Returns:
        str: ダウンロードして保存された音声ファイル名
    """
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    return filename

def convert_mp3_to_monowav(filename: str)->str:
    """mp3の動画をwavに変換する

    Args:
        filename (str): 変換対象のmp3のファイル名。

    Returns:
        str: 変換されたwavファイル名
    """
    # 一旦固定
    output_filename = "samples/test.wav"
    
    try: 
        aud_seg = AudioSegment.from_mp3(filename.replace('.m4a', '.mp3'))
        ext_aud_seg = aud_seg.set_channels(1)
        ext_aud_seg = ext_aud_seg.set_frame_rate(16000)
        ext_aud_seg.export(output_filename,format="wav")
        
        return output_filename
    except Exception as e:
        print(e)
        exit -1
        
def convert_wav_to_base64(filename: str) -> bytes:
    """Clova API用にwavファイルをbytes形式に変換する。

    Args:
        filename (str): 変換対象のwavファイル名

    Returns:
        bytes: wavをbytesに変換したファイル
    """
    return open(filename, "rb").read()
        
def clova_recognition(endpoint: str, apikey: str, audio_content: bytes)->str:
    """音声をclova apiで書き起こす。

    Args:
        endpoint (str): Clova APIのエンドポイント
        apikey (str): Clova APIの認証キー
        audio_content (bytes): 検出対象の音声のbytes
    """
    my_uuid= str(uuid.uuid4())
    print(f"endpoint :{endpoint}, apikey :{apikey}, uuid :{my_uuid}")
    
    recognition_request = RecognitionRequest(
        recognition_id=my_uuid,
        config = RecognitionConfig(
            api_key = apikey,
            audio_format = AUDIO_L16_RATE_8000_CHANNELS_1,
            language = JA,
        ),
        audio_content = audio_content
    )
    
    with grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = RecognizerStub(channel)
        response = stub.Recognize(recognition_request)
    
    return response.result.text

def load_clova_env(envfile: str = ".env") -> [str, str]:
    """ローカルのenvファイルからclova apiの認証情報を取得する。

    Args:
        envfile (str, optional): _description_. Defaults to ".env")->(str.

    Returns:
        (str, str): _description_
    """
    load_dotenv(envfile)
    return os.environ['ENDPOINT'],os.environ['API_KEY']
            
def main(url: str):
    if re.match("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", url):
        print("youtubeから音声ファイルをダウンロードします。")
        filename = download_youtube(url)
    elif os.path.exists(url):
        print("ローカルのmp3ファイルを利用します。")
        filename = url
    else:  
        print("Error")
        exit -1
    
    filename = convert_mp3_to_monowav(filename)

    clova_endpoint, clova_api_key=load_clova_env()
    result = clova_recognition(
        endpoint=clova_endpoint,
        apikey=clova_api_key,
        audio_content=convert_wav_to_base64(filename)
    )
    print(f"検出結果: {result}")


if __name__ == "__main__":
    # 引数の設定
    parser = argparse.ArgumentParser()
 
    parser.add_argument(
        "--url",
        type=str,
        help="Youtubeの動画のパス",
    )
    args = parser.parse_args()
 
    main(
        url=args.url
    )
