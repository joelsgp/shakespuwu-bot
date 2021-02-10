import json
from uwu import owoify
import tweepy


TWEET_CHAR_LIMIT = 280
CHUNKS_FILE_PATH = 'shakespuwu.json'


def blob_to_owo_list(in_file_path='shakespeare.txt',
                     out_file_path=CHUNKS_FILE_PATH,
                     interval=TWEET_CHAR_LIMIT):
    text_chunks = []
    with open(in_file_path, encoding='utf-8') as in_file:
        while True:
            read_text = in_file.read(interval)
            if not read_text:
                break
            else:
                text_chunks.append(read_text)

    text_chunks = [owoify(t) for t in text_chunks]

    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(text_chunks, out_file)

    return text_chunks


try:
    with open(CHUNKS_FILE_PATH, encoding='utf-8') as chunks_file:
        passages = json.load(chunks_file)
except FileNotFoundError:
    passages = blob_to_owo_list()


with open('auth.json') as auth_file:
    auth_dict = json.load(auth_file)


auth = tweepy.OAuthHandler(auth_dict['consumer_key'], auth_dict['consumer_secret'])
auth.set_access_token(auth_dict['access_token'], auth_dict['access_token_secret'])

api = tweepy.API(auth)
