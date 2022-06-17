SITE = 'https://developer.twitter.com/en/portal/projects/1520753611042861056/apps/24143236/keys'

api_key = 'dvB7ZgmaVH9ftZ5CiAaaWoYP9'
api_key_secret = 'slOYkQ2nVmSjvJMb6J1ILYR14wauUreJrcM8J0YCjo9UfyT2iE'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIRlcAEAAAAADdXHkL9H7vOefRP2YGue77Cx1DI%3Dm7O6Pycqsjdh53z3cEtd2cy7O7vExjT3e1tJrd70aKB5XEVMD2'


access_token_key = '818886006866726912-2FdGaRN9ubI4HW0IRp2TUT4A9kn2cNP'
access_token_secret = 'L7Fx7Qx8wAyaLLRt3quzie3UwZOaj3fbsKY2Oy9AlHgaT'

import twitter as t

t_api = t.Api(consumer_key=api_key,
              consumer_secret=api_key_secret,
              access_token_key=access_token_key,
              access_token_secret=access_token_secret)


def get_texts(query,count):
    words = []
    statuses = t_api.GetSearch(term=query, count=count)
    for status in statuses:
        words.append(status.text)

    return words

def write_texts(word,texts):
    with open(f'{word}_twitter.txt','a',encoding='utf-8') as f:
        for text in texts:
            f.writelines(text+'\n')