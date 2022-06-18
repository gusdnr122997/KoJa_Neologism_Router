# 한일 신조어 사전 및 한일 신조어 유사도 도출 시스템 구축 (부제: MUSE를 활용한 한일 신조어 워드 임베딩)
**Team Router**
* 전현욱(팀장): 프로젝트 설계, FastText 단어 임베딩, MUSE, 데이터 전처리, 데이터 수집 Logic
* 김우영(팀원): 데이터 수집 Logic, 데이터 전처리, 데이터 분석, 데이터 수집
* 이사무엘(팀원): HTML/CSS, Flask 개발, 데이터 수집
* 심하영(팀원): DB 설계, Flask 개발, 데이터 수집

# 개요
* 기간: 2022.03.07~2022.06.20
* 신조어가 포함된 한국어와 일본어의 워드 임베딩을 통해 Source 신조어와 가장 유사한 Target 신조어를 도출한다.
* 결과를 Web으로 표시해 서비스 가능하도록 만든다.

# 배경

밀레니얼(Millennial) 세대들의 사회 진출, 인터넷의 다양화에 따라서 그에 맞게 ‘신조어’ 들도 각양각색으로 발생하고 있다. 최
근에는 메타버스(Meta-verse)의 확장으로인터넷상에서외국인들과의교류가 늘어나면서 대화할 기회가 많아졌다. 그러나
이들이 사용하는 신조어는 우리에게 알아 듣기가 어려우며, 그들도 우리의 신조어를 이해하기 어려울 것이다. 현재의 [네이버 파파고](https://papago.naver.com/) 와 [구글 번역기](https://translate.google.co.kr/) 같은 번역기는 이러한 신조어가 번역이 잘 안 된다는 단점이 있다. 우리는 이러한 문제를 해결해 보고자 NLP의 기초가 되는 워드 임베딩을 통해 신조어 사이의 유사도를 도출하는 프로젝트를 진행하게 되었다. 또한 이를 사용자에게 제공하려는 목적으로 Web을 통해 서비스를 하려고 한다.

# 결과요약
2022.06.17 시점에서 정확도 약 40%를 도출했다. 낮은 정확도에 대한 원인은 다음과 같이 분석해 보았다
* 데이터 전처리 과정에서, 특히 커뮤니티 특성상 데이터에 **미사여구**가 굉장히 많았다. 광고성 내용, 문맥에 맞지 않는 단어선택 등 다양한 케이스가 많았다. 실제로 크롤링으로 가져온 한국어 문장 데이터는 100만이 넘었지만, 전처리 과정을 거치고 나니 약 20만, 1/5정도로 줄어들었다.


* 데이터 대상이 되는 커뮤니티는 총 4개(디씨인사이드, 네이트판, tanuki, twitter)지만, 각 커뮤니티 특성이 강하게 반영된다는 점이 있었다. 실제로 '보이루' (보겸 + 하이루) 라는 신조어를 대상으로 데이터를 수집했을 떄, 디씨인사이드와 네이트판의 주변 단어들의 유사성이 거의 없었다.


# 데이터 정의
* 한국어: 232,342문장 (디씨인사이드, 네이트판)
* 일본어: 121,032문장 (tanuki, Twitter)
  
# 폴더 설명
* DataCrawling: 데이터 수집
* ML: Aligned Embeddings의 결과물 + 모델 학습 주피터 노트북 파일 포함
* mecab-ja: MeCab-ipadic-Neologd 형태소 분석기가 포함된 일본어 데이터 전처리
* mecab-ko: konlpy-mecab 사용자 사전 형태소 분석기가 포함된 한국어 데이터 전처리
* Web: Flask App

****

References
* [MUSE](https://github.com/facebookresearch/MUSE)
* [FastText](https://github.com/facebookresearch/fasttext)
* [일본어 Pre-Trained FastText Model](https://github.com/lounlee/fasttext_jpn_model_neologd)
* [mecab-ipadic-neolodg](https://github.com/neologd/mecab-ipadic-neologd)
* [koNLPy](https://github.com/konlpy/konlpy)
