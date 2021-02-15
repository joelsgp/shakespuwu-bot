import json
import time
from pathlib import Path

import uwu

import tweepy


TEXT_FOLDER = Path('text')
SOURCE_FILE_PATH = TEXT_FOLDER / 'shakespeare.txt'
CHUNKS_FILE_PATH = TEXT_FOLDER / 'shakespeare-chunks.json'
INDEX_FILE_PATH = TEXT_FOLDER / 'index.json'
AUTH_FILE_PATH = 'auth.json'

TWEET_CHAR_LIMIT = 280
# ten minutes
TWEET_INTERVAL_SECONDS = 600

RUN_FOREVER = True


def blob_to_list(in_file_path=SOURCE_FILE_PATH,
                 out_file_path=CHUNKS_FILE_PATH,
                 interval=TWEET_CHAR_LIMIT):
    with open(in_file_path, encoding='utf-8') as in_file:
        read_text = in_file.read()

    text_chunks = [read_text[i:i+interval] for i in range(0, len(read_text), interval)]

    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(text_chunks, out_file)

    return text_chunks


def load_passages(file_path=CHUNKS_FILE_PATH):
    try:
        with open(file_path, encoding='utf-8') as chunks_file:
            passages = json.load(chunks_file)
    except FileNotFoundError:
        passages = blob_to_list()

    return passages


def next_passage(passages, index_file_path=INDEX_FILE_PATH):
    try:
        with open(index_file_path) as index_file:
            index = json.load(index_file)
    except FileNotFoundError:
        index = 0
    print(f'Got index {index}')

    try:
        passage = passages[index]
    except IndexError:
        return None
    else:
        passage = uwu.owoify(passage)

    index += 1
    with open(index_file_path, 'w') as index_file:
        json.dump(index, index_file)
    print(f'Saved new index {index}')

    return passage


def run_once(api, passages):
    content = next_passage(passages)
    if content is None:
        print('Done!')
    else:
        api.update_status(content)
        # tweet_status = api.update_status(content)
        # print(tweet_status)
        print(f'Tweeted: \n{content}\n')


def main():
    # load twitter stuff
    with open(AUTH_FILE_PATH) as auth_file:
        auth_dict = json.load(auth_file)

    auth = tweepy.OAuthHandler(auth_dict['consumer_key'], auth_dict['consumer_secret'])
    auth.set_access_token(auth_dict['access_token'], auth_dict['access_token_secret'])

    api = tweepy.API(auth)

    # load text
    passages = load_passages()

    if RUN_FOREVER:
        while True:
            run_once(api, passages)

            print(f'Sleeping for {TWEET_INTERVAL_SECONDS} seconds.')
            time.sleep(TWEET_INTERVAL_SECONDS)

    else:
        run_once(api, passages)


if __name__ == '__main__':
    main()
