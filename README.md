커뮤니티 게시물 분석
============

사용 모듈
------------
* 사용중
    import requests
    from bs4 import BeautifulSoup

    import json
    import os
    import time
    from google.colab import output
    from fake_useragent import UserAgent
* 사용예정
    None

진행 단계
------------
1. 스크래퍼 제작, 스크래핑 진행
2. 데이터 전처리
* 데이터 토큰화
* 유사 단어 판별
3. 머신 러닝 or 딥러닝 진행
* 머신러닝: 게시글 댓글수, 추천수 예측
* 딥러닝: 게시글 생성

진행
------------
* 스크래퍼 제작 완료, 스크래핑 진행 중

추가 진행 목표
------------
* Dcinside에 종속된 코드 부분을 분리 후 모듈화,
* 다른 커뮤니티 클래스 제작
