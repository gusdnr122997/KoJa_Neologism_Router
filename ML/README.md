# FastText Embedding And MUSE Bilingual Word Embeddings Alignment

**실행환경**
* Google Colab Pro
* [FastText](https://github.com/facebookresearch/fasttext)
* [MUSE](https://github.com/facebookresearch/MUSE)
* Flask

**Pre-Trained Model**
* [wiki.ko.bin](https://drive.google.com/file/d/1FQ0ooFyx2uMQR1cz3Mxl-YIn7L97wIDz/view?usp=sharing)
* [ja_model.bin](https://drive.google.com/file/d/1ED7o_h3KO3fKcDSRHXiuAFL3fxEM5z78/view) # Created by [lounlee](https://github.com/lounlee/fasttext_jpn_model_neologd)

**결과물**
* [vectors-ja.txt](https://drive.google.com/file/d/1MM3iES-v0sqfFIjbbwuPY9BukpQnDNOO/view?usp=sharing)
* [vectors-ko.txt](https://drive.google.com/file/d/1qWiPm5GTqVdlEKpDxunuSY2CLDAZASHK/view?usp=sharing)

**폴더 설명**
* ipynb: 구글 colab에서 실행할 주피터 노트북 파일 존재
* muse_dict_ko-ja: MUSE alignment를 위한 Dictionary Files
* vecs : 결과물을 저장하는 Directory

**파일 설명**
* ft_vecs.py: vecs 폴더에 있는  워드 임베딩 파일을 읽고 nearest neighbor + similarity 기능을 REST API를 통해 제공

**실행**
* 학습절차: ipynb/GENSIM+FASTTEXT+MUSE.ipynb 파일을 순차적으로 실행
  * git clone MUSE 후 muse_dict_ko-ja 폴더에 있는 파일들을 꼭 MUSE 디렉터리에 넣어야 함! 자세한 내용은 주피터 노트북 파일 참고
* ft_vecs.py를 실행하면 서비스 WEB에서 신조어 유사도 정보를 가져올 수 있다. 

****
Developed By:
  * 전현욱