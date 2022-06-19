# Web for KOJA_NEOLOGISM_DICTIONARY

**실행환경**
* Windows 10
* Python 3.9
  * Anaconda 사용 권장
* Python Libraries:
  * Flask
  * Flask-SQLAlchemy
  * SQLite3
  * pywin32
  
**폴더 설명**
* data: 신조어 단어 사전 데이터
* static: css 및 icons
* templates: html

**파일 설명**
* db.sqlite: db 파일
* admin_country.py: DB 초기화 후 필수 데이터 INSERT
* db_inser.py: data/신조어_진행상황.xlsx를 바탕으로 db에 사전 데이터 INSERT
* models.py: db.sqlite의 DB 설계
* app.py: Flask 실행


**실행**

app.py 실행

****
Developed By:
  * 전현욱: Web 기능 설계
  * 이사무엘: HTML/CSS 개발, Flaks 개발
  * 심하영: DB 설계, Flask 개발