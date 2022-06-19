from flask import *
from models import *

import random

import os, datetime, json, requests

app = Flask(__name__)
searchkey = None

def make_api_form(word,country,num=10):
    json_format = {
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'word': word,
        'country': country,
        'num': num
    }
    return json_format

@app.route('/',methods=['GET','POST'])
def main():
    username = session.get('name',None)
    if request.method == 'POST':
        searchkey = request.form['searchkey']
        if username:
            session['searchkey'] = searchkey
        return redirect('/result?searchkey='+searchkey)
    return render_template('index.html', username=username)

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('name',None)
    session.pop('user_code',None)
    session.pop('searchkey',None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_request = request.form
        r_id = user_request['id']
        r_pw = user_request['pw']
        user = User.query.filter_by(id=r_id).first()
        if not user:
            flash("존재하지 않은 ID입니다")
        else:
            if r_pw != user.pw:
                flash("비밀번호가 틀렸습니다")
            else:
                # 로그인 검증 완료
                session.clear()
                session['user_code'] = user.user_code
                session['name'] = user.name
                session['searchkey'] = None
                return redirect('/')
    return render_template('login.html')


@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        user_request = request.form
        
        user_id = User.query.filter_by(id=user_request['id']).first()
        user_email = User.query.filter_by(email=user_request['email']).first()

        if not user_id and not user_email:
            user = User()
            user.id = user_request['id']
            user.pw = user_request['pw']
            user.name = user_request['name']
            user.email = user_request['email']
            db.session.add(user)
            db.session.commit()
            flash('회원가입 완료')
        if user_id:
            flash("중복된 아이디입니다.")
        elif user_email:
            flash("중복된 이메일입니다.")

        return render_template('login.html')

@app.route('/result',methods=['GET','POST'])
def result():
    username = session.get('name',None)
    if request.method == 'POST':
        search_form = request.form
        searchkey = search_form['searchkey']
        if username:
            session['searchkey'] = searchkey
        return redirect('?s='+searchkey)

    searchkey = request.args['searchkey'] if 'searchkey' in request.args else None
    if searchkey == None:
        return render_template('result.html')
    else:
        if username:
            session['searchkey'] = searchkey
        found_word = Dic.query.filter_by(word=searchkey).all()
        if len(found_word) == 0:
            return render_template('result.html', searchkey=searchkey, username=username)
        else:
            meanings = (found_word[0].meaning,found_word[0].meaning_jp)
            r_result = requests.post(
                url='http://127.0.0.1:8080/get_nn',
                json=make_api_form(found_word[0].word,found_word[0].language_code,50)
            )
            similar_words = {
                'kwords':[],
                'jwords':[]
            }
            if r_result.status_code == 200:
                r_result_content = json.loads(r_result.content)
                if r_result_content['result_k'] is not False:
                    if found_word[0].language_code == 1:
                        for score, simword in r_result_content['result_k'][:10]:
                            if score >= 100:
                                continue
                            similar_words['kwords'].append((simword, score))
                    else:
                        for score, simword in r_result_content['result_k']:
                            if score >= 100:
                                continue
                            if simword in kwords:
                                if score > 55:
                                    similar_words['kwords'].append((simword,score))
                if r_result_content['result_j'] is not False:
                    if found_word[0].language_code == 2:
                        for score, simword in r_result_content['result_j'][:10]:
                            if score >= 100:
                                continue
                            similar_words['jwords'].append((simword,score))
                    else:
                        for score, simword in r_result_content['result_j']:
                            if score >= 100:
                                continue
                            if simword in jwords:
                                if score > 55:
                                    similar_words['jwords'].append((simword,score))

            return render_template('result.html',searchkey=searchkey,meanings=meanings, username=username, found_word=found_word, similar_words=similar_words,kwords=kwords,jwords=jwords)

@app.route('/words',methods=['GET'])
def words():
    usercode = session.get('user_code',None)

    if not usercode:
        return redirect('/login')
    else:
        page = request.args.get('page', type=int, default=1)  # 페이지

        vocab = Vocab.query.filter_by(user_code=usercode).paginate(page=page, per_page=5)

    return render_template('words.html',paginate=vocab)

@app.route('/quiz',methods=['GET','POST'])
def quiz():
    usercode = session.get('user_code',None)

    if request.method == 'POST':
        answer_word = list(request.form.items())[0][0]
        selected_word_code = int(list(request.form.items())[1][0])

        answer_word_code = Dic.query.filter_by(word=answer_word).first().code

        if answer_word_code == selected_word_code:
            correct = True
        else:
            correct = False
        print(1,correct)
        return render_template('quiz.html',correct=correct,asnwer=None)

    if not usercode:
        return redirect('/login')
    
    words = Dic.query.filter_by(language_code=1).all()

    answer = random.choice(words)
    words.remove(answer)

    wrong_list = []
    for _ in range(3):
        wrong_list.append(random.choice(words))

    choices = wrong_list + [answer]
    random.shuffle(choices)

    # 일본어 퀴즈
    words_jp = Dic.query.filter_by(language_code=2).all()
    answer_jp = random.choice(words_jp)
    words_jp.remove(answer_jp)
    
    wrong_list_jp = []
    for _ in range(3):
        wrong_list_jp.append(random.choice(words_jp))

    choices_jp = wrong_list_jp + [answer_jp]
    random.shuffle(choices_jp)

    print(2,answer)
    return render_template('quiz.html',answer=answer,answer_jp=answer_jp,choices=choices,choices_jp=choices_jp)


@app.route('/new_word', methods=['POST'])
def new_word():
    usercode = session.get('user_code', None)
    if not usercode:
        return redirect('/login')
    if request.method == 'POST':
        searchkey = session.get('searchkey',None)
        print(searchkey)
        dic = Dic.query.filter_by(word=searchkey).first()
        isInVocab = Vocab.query.filter_by(user_code=usercode,word_code=dic.code).first()
        print(isInVocab)
        if isInVocab:
            flash('이미 추가한 단어입니다')
        else:
            vocab = Vocab()
            vocab.user_code = usercode
            vocab.word_code = dic.code
            vocab.word = dic.word
            vocab.meaning = dic.meaning
            vocab.meaning_jp = dic.meaning_jp
            db.session.add(vocab)
            db.session.commit()
            flash('단어가 추가되었습니다')
        return redirect('/result?searchkey='+searchkey)

    
@app.route('/del_word', methods=['POST'])
def del_word():
    usercode = session.get('user_code', None)
    if not usercode:
        return redirect('/login')
    if request.method == "POST":
        wc = int(list(request.form.items())[0][0])
        Vocab.query.filter_by(word_code=wc).delete()
        db.session.commit()
        flash('단어를 삭제했습니다.')
    return redirect('/words')


@app.route('/introduce',methods=['GET'])
def introduce():
    username = session.get('name',None)
    return render_template('introduce.html', username=username)

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir,'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'

    db.init_app(app)
    db.app = app
    db.create_all()

    kwords = [x.word for x in Dic.query.filter_by(language_code=1).all()]
    jwords = [x.word for x in Dic.query.filter_by(language_code=2).all()]

    app.run(host='0.0.0.0',port=80,debug=True)