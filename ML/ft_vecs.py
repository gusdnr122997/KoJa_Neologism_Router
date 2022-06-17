import io
import numpy as np

src_path = 'vecs/vectors-ko.txt'
tgt_path = 'vecs/vectors-ja.txt'

def load_vec(emb_path, nmax=50000):
    vectors = []
    word2id = {}
    with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        next(f)
        for i, line in enumerate(f):
            word, vect = line.rstrip().split(' ', 1)
            vect = np.fromstring(vect, sep=' ')
            assert word not in word2id, 'word found twice'
            vectors.append(vect)
            word2id[word] = len(word2id)
            if len(word2id) == nmax:
                break
    id2word = {v: k for k, v in word2id.items()}
    embeddings = np.vstack(vectors)
    return embeddings, id2word, word2id


nmax = 2000000  # maximum number of word embeddings to load
src_embeddings, src_id2word, src_word2id = load_vec(src_path, nmax)
tgt_embeddings, tgt_id2word, tgt_word2id = load_vec(tgt_path, nmax)

def get_nn_full(word, src_emb, src_id2word, tgt_emb, tgt_id2word, K=5):
    try:
        print("Nearest neighbors of \"%s\":" % word)
        word2id = {v: k for k, v in src_id2word.items()}
        word_emb = src_emb[word2id[word]]
        scores = (tgt_emb / np.linalg.norm(tgt_emb, 2, 1)[:, None]).dot(word_emb / np.linalg.norm(word_emb))
        k_best = scores.argsort()[-K:][::-1]
        result = []
        for i, idx in enumerate(k_best):
            print('%.4f - %s' % (scores[idx], tgt_id2word[idx]))
            result.append((round(scores[idx]*100,3), tgt_id2word[idx]))
    
        return result
    except:
        return False

def get_similarity(word1, word2, src_emb, src_id2word, tgt_emb, tgt_id2word):
    try:
        print("Similarity between \"%s\" and \"%s\":" % (word1,word2),end=" ")
        word2id1 = {v: k for k, v in src_id2word.items()}
        word1_emb = src_emb[word2id1[word1]]
        word2id2 = {v: k for k, v in tgt_id2word.items()}
        word2_emb = tgt_emb[word2id2[word2]]
        scores = (word2_emb / np.linalg.norm(word2_emb)).dot(word1_emb / np.linalg.norm(word1_emb))
        print(round(scores,4))
        return round(scores,4)
    except:
        return False


def get_sim(word1,word2):
    score = get_similarity(word1,word2,src_embeddings,src_id2word,tgt_embeddings,tgt_id2word)
    if score:
        return score

def get_nn(word,k=10):
    result = get_nn_full(word, src_embeddings, src_id2word, tgt_embeddings, tgt_id2word, K=k)
    if result:
        return result

from flask import *

app = Flask(__name__)

@app.route('/get_nn',methods=['POST'])
def get_nn_api():
    request.form['text']

app.run(host='0.0.0.0',port='8080')
