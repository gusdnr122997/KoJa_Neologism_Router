# COMMUNITY PLATFORM 검색어 크롤링 Task

**실행환경**
* Windows 10
* Python 3.9
  * Anaconda 사용 권장
* Python Libraries:
  * psutil
  * Selenium
  * BeautifulSoup
  * twitter api

**개발완료된 Platform 목록**
* 한국
  * 디시인사이드 (DC)
  * 네이트판 (PANN)
* 일본
  * Tanuki (tanuki)
  * Twitter (twitter)
  
**폴더 설명**
* links: 키워드 단어의 links.txt를 모아놓은 폴더
  * BeautifulSoup Parsing을 위한 폴더
* rawdata: 키워드 단어에 대한 문장을 긁어온 _Platform.txt 폴더
  * 결과물(Result)

**파일 설명**
* Platform.py: 신조어목록.txt를 대상으로 Platform에서 데이터 크롤링 시작
  * ex) DC.py > DC에서 신조어목록 단어들이 포함된 내용 가져오기
* twitter_crawling.py : 트위터 API를 통한 Crawling이지만, API Key를 발급받아야만 사용할 수 있다.
* 신조어목록.txt: 검색 대상 신조어를 한 열로 나열
* bs4_crawling: links 폴더의 파일들을 대상으로 해당 Link의 HTML을 파싱 후 rawdata에 존재하는 해당 Keyword 문장 append
* check_data_length.py: 각 Keyword의 문장데이터 개수 카운팅
* chromedriver.exe: Selenium 모듈에서 사용할 크롬드라이버
  * 주의! 크롬이 설치되어 있어야 하며 크롬 버전에 알맞는 크롬드라이버를 다운로드 받아야한다.
  * 크롬드라이버 다운로드 사이트: https://chromedriver.chromium.org/downloads


**실행순서**
1. 신조어목록.txt에 크롤링할 Keyword를 추가한다 (하드웨어 고려해서 키워드 개수 제한)
2. 원하는 커뮤니티 플랫폼 파일을 실행한다
3. rawdata의 결과물을 확인한다

****
Developed By:
  * 전현욱: Logic 설계, BS4 프로세스 개발
  * 김우영: DC,PANN,Tanuki 프로세스 개발