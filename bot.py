import json
import time
from uwu import owoify
import tweepy


TWEET_CHAR_LIMIT = 280
CHUNKS_FILE_PATH = 'shakespuwu.json'
INDEX_FILE_PATH = 'index.json'

# ten minutes
TWEET_INTERVAL_SECONDS = 600


def blob_to_owo_list(in_file_path='shakespeare.txt',
                     out_file_path=CHUNKS_FILE_PATH,
                     interval=TWEET_CHAR_LIMIT):
    with open(in_file_path, encoding='utf-8') as in_file:
        read_text = in_file.read()

    owo_text = owoify(read_text)
    text_chunks = [owo_text[i:i+interval] for i in range(0, len(owo_text), interval)]

    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(text_chunks, out_file)

    return text_chunks


def load_passages(file_path=CHUNKS_FILE_PATH):
    try:
        with open(file_path, encoding='utf-8') as chunks_file:
            passages = json.load(chunks_file)
    except FileNotFoundError:
        passages = blob_to_owo_list()

    return passages


def next_passage(passages, index_file_path=INDEX_FILE_PATH):
    try:
        with open(index_file_path) as index_file:
            index = json.load(index_file)
    except FileNotFoundError:
        index = 0

    try:
        passage = passages[index]
    except IndexError:
        return None

    index += 1
    with open(index_file_path, 'w') as index_file:
        json.dump(index, index_file)

    return passage


def main():
    # load twitter stuff
    with open('auth.json') as auth_file:
        auth_dict = json.load(auth_file)

    auth = tweepy.OAuthHandler(auth_dict['consumer_key'], auth_dict['consumer_secret'])
    auth.set_access_token(auth_dict['access_token'], auth_dict['access_token_secret'])

    api = tweepy.API(auth)

    # load text
    passages = load_passages()

    while True:
        content = next_passage(passages)
        if content is None:
            print('Done!')
        else:
            api.update_status(content)
            print(f'Tweeted: {content}')

        print(f'Sleeping for {TWEET_INTERVAL_SECONDS} seconds.')
        time.sleep(TWEET_INTERVAL_SECONDS)


if __name__ == '__main__':
    main()
