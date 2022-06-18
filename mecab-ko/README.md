# MeCaB-KO

**실행환경**
* Windows 10
* Python 3.7
  * Anaconda 사용 권장
* Python Libraries:
  * pywin32
  * [koNLPy](https://github.com/konlpy/konlpy)
  * [mecab-python-wheel](https://github.com/Pusnow/mecab-python-msvc/releases/tag/mecab_python-0.996_ko_0.9.2_msvc-2)
* [mecab-ko-msvc](https://github.com/Pusnow/mecab-ko-msvc/releases/tag/release-0.9.2-msvc-3)

**폴더 설명**
* before: 크롤링해서 모은 비정형 데이터 폴더
* after: 데이터 전처리 후 결과 폴더 (ko_시간.xlsx 형태로 나옴)
* whls: 설치해야할 python-wheel 폴더

**파일 설명**
* kopersons.txt: 인물사전에 새롭게 추가할 인물을 추가하기 위한 텍스트 파일
* kowords.py: 사전에 새롭게 추가할 단어를 추가하기 위한 텍스트 파일, 태그는 명사로 추가
* 한국어불용어.txt: 한국어 불용어를 모아놓은 텍스트 파일
* add_dict_noun.py: kowords.txt를 바탕으로 사용자 사전에 단어를 추가
* add_dict_person.py: kopersons.txt를 바탕으로 사용자 사전에 인명을 추가
* ko_dataprocess.py: before 폴더의 데이터 전처리 시작, after에 xlsx 확장자로 저장


**실행순서**

사전 구축 및 실행은 [여기](https://luminitworld.tistory.com/104) 를 참고

****
Developed By:
  * 전현욱: 데이터 전처리 Logic 개발
  * 김우영: 데이터 분석, 불용어 정의, 사용자 사전 추가 대상 단어 선정