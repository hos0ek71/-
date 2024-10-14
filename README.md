import tkinter as tk # Tkinter 라이브러리를 사용하여 GUI 를 구현하기 위해 import
from tkinter import scrolledtext, messagebox # 스클롤 가능한 텍스트 박스와 메시지 박스 사용을 위해 import
import requests # HTTP 요청을 보내기 위해 requests 라이브러리 사용
import time # API 요청간 딜레이를 추가하기 위해 time 라이브러리 사용

# 뉴스 검색 API 호출 함수
def get news(quesry, clinet_id, client_secret, display=10, start=1):
  """
  네이버 뉴스 검색 API를 호출하여 뉴스 데이터를 반환하는 함수
  :param query:  검색할 키워드
  :param client: 사용자가 입력한 네이버 API Client ID
  :param client_secret: 사용자가 입력한 네이버 API Client Secret
  :param display: 한번에 보여줄 결과 수 (기본10, 최대 100)
  :param start: 검색 결과의 시작 위치 (페이지 기능을 구현)
  :return: 뉴스 검색 결과 리스트
  """
  url = 'https://openapi.naver.com/v1/search/news.json' # 네이버 뉴스 검색 API URL
  header = {
  'X-Naver-Client-id': clinet_id, # API 호출 시 필요한 Clinet ID
  'X-Naver_Client-Secret: client_secret # API 호출시 필요한 Client Secret
  }
  params = {
        'query': query
