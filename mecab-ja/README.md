# MeCaB-JA

**실행환경**
* Windows 10
* Windows Ubuntu 20.04.4 LTS
* Python 3.7
  * Anaconda 사용 권장
* Python Libraries:
  * mecab-python3
* [MeCab 0.996](https://github.com/ikegami-yukino/mecab/releases/download/v0.996.2/mecab-64-0.996.2.exe)
* [mecab-ipadic-neologd](https://github.com/neologd/mecab-ipadic-neologd)

**폴더 설명**
* before: 크롤링해서 모은 비정형 데이터 폴더
* after: 데이터 전처리 후 결과 폴더 (ja_시간.txt 형태로 나옴)

**파일 설명**
* 일본어불용어.txt: 일본어 불용어를 모아놓은 텍스트 파일
* ja_dataprocess.py: before 폴더의 데이터 전처리 시작, after에 txt 확장자로 저장

**실행순서**

사전 구축 및 실행은 [여기](https://qiita.com/ku_a_i/items/cf9fc9636958adafc690) 를 참고

****
Developed By:
  * 전현욱: 데이터 전처리 Logic 개발
  * 김우영: 데이터 분석, 불용어 정의