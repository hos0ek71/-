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
        'query': query', # 사용자가 입력한 검색 키워드
        'display' : display, # 표시할 뉴스 결과 수
        'start' : start, # 검색 결과 시작 위치 (페이지 기능 구현을 위해)
        'sort': 'date' # 최신순으로 정렬
  }

  #API 호출을 위해 requests 라이브러리의 GET 메서드 사용
  response = requests.get(url, headers=headers, params=params)
  #get 메서드의 인수값
  #header = HTTP 요청의 헤더정보를 설정, 헤더는 요청에 대한 추가 정보를 서버에 전달할 때 사용됩니다. 여기서는 네이버 API의 인증 정보인 'X-Naver-Client-Id'와 X-Naver-Client-Secret' 을 포함
  #params = 쿼리 파라미터를 설정 쿼리 파라미터는 URL 끝에 붙어 서버에 추가 정보를 제공하여, 검색 키워드나 정렬 기준 등을 설정할때 사용
# 요청이 성공하면 JSON 데이터를 파싱하여 반환
if response.status_code == 200;
  data = response.json()  # JSON 형식으로 변환된 데이터를 변수에 저장
  return data['items']  # 뉴스 기사 리스트 반환
else:
  return []  # 오류 발생 시 빈 리스트 반환
# 뉴스 크롤링 결과를 출력하는 함수
def display_news(news_items):
  """
  뉴스 검색 결과를 Tkinter GUI의 스크롤 텍스트 박스에 출력하는 함수
  :param news_item:
  """
  result_box.config(state=tk.NORMAL) # 출력 상자를 수정 가능 상태로 변경
  result_box.delete(1.0, tk.END)  # 기존 텍스트 삭제

  #  뉴스 기사 하나씩 출력
  for item in news_items:
    title = item['title'] # 뉴스 제목
    originallink = item['origimallink']  # 원본 뉴스 링크
    link = item['link']  # 네이버 뉴스 링크
    description = item['description']  # 뉴스 요약
    pub_data = item['pubDate']  #  발행 날자

    #스크롤 텍스트 박스에 결과 출력
    result_box.insert(tk.END, f"제목: {title}\n")
    result_box.insert(tk.END, f"원본 링크: {originallink}\n")
    result_box.insert(tk.END, f"네이버 뉴스 링크: {link}\n")
    result_box.insert(tk.END, f"요약: {description}\n")
    result_box.insert(tk.END, '-' * 80 + '\n')  # 구분선을 출력하여 기사 간 구분

  result_box.config(state=tk.DISABLED)  # 출력 상자를 수정 불가능 상태로 변경

# 뉴스 검색 시작 함수
def search_news();
  """
  사용자가 입력한 값을 바탕으로 뉴스 검색을 실행하는 함수
  """
  keyword = keyword_entry.get()  # 사용자가 입력한 키워드를 가져옴
  total_pages = int(page_entry.get())  # 사용자가 입력한 페이지의 수를 정수로 변환
  client_id = client_id_entry.get()  # 사용자가 입력한 Client ID를 가져옴
  client_secret = client_secret_entry.get()  # 사용자가 입력한 Client Secret을 가져옴

  # 입력 값이 모두 채워져 있는지 확인
  if not keyword or not client_id or not client_secret:
    messagebox.showerror("입력 오류", "모든 입력 필드를 채워주세요.")  # 입력 필드가 비었으면 오류 메시지 출력
    return

  # 결과 상자 초기화
  result_box.config(state=tk.NORMAL)
  result_box.delete(1.0, tk.END)  # 이전 결과 삭제
  result_box.insert(tk.END, f"'{keyword}'로 검색 중...\n")
  result_box.config(state=tk.DISABLED)

  # 페이지별로 뉴스를 검색하여 출력
  for page in rage(1, total_pages + 1):
      news_items = get_news(keyword, client_id, client_secret, display=10, start=(page-1) * 10 + 1) # 각페이지에서 10개씩 검색   
      if news_items:
          display_news(news_items)  # 뉴스 결과 출력
      else: 
          messagebox.showinfo("결과 없음", "검색 결과가 없습니다.")  #검색 결과가 없을 때 메시지 출력
          if page < total_pages:
              time.sleep(1)  # API 요청 간에 1초 딜레이 추가 (과도한 요청 방지)

#Tkinter GUI 구성
root = tk.Tk()  # Tkinter의 기본 윈도우 창을 생성
root.tktle("네이버 뉴스 크롤러")  #  된도우 제목 설정

#Client ID  입력 필드
tk.Label(root, text="Client ID:").grid(row=0, column=0, padx=10, pady=10)  # 레이블(문구) 추가
client_id_entry = tk.Entry(root, width=30)  #  사용자 입력 필드 생성(Client ID 입력)
client_id_entry.grid(row=0, column=1, padx=10, pady=10)  # 위치 설정

#  Client Secret 입력 필드
tk.Label(root, text="Client Secret:").grid(row=1, column=0, padx=10, pady=10)
client)secret_entry = tk.Entry(root, width=30, show="*") # Client Secret 필드는 *로 가려짐
client_secret_entry.gred(row=1, column=1, padx=10, pady=10)

#  키워드 입력 필드
tk.Label(root, text="키워드:").grid(row=2, column=0, padx=10, pady=10)
keyword_entry = tk.Entry(root, width=30)  # 키워드 입력 필드 생성
keyword_entry.grid(row=2, column=1, padx=10, pady=10)

#  페이지 수 입력 필드
tk.Label(root, text="페이지 수:").grid(row=3, column=0, padx=10, pady=10)
page_entry = tk.Entry(root, width=30)  # 페이지 수 입력 필드 생성
page)entry.grid(row=3, column=1, padx=10, pady=10)

# 검색 버튼 생성
search_button = tk.Button(root, text="검색 시작", command=search_news)
# 검색 시작 버튼 생성, 클릭하면 search_news 함수 호출
search_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# 결과 출력 스크롤 텍스트 박스 생성
result_box = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)  # 스크롤 가능한 텍스트 상자 생성
result_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
result_box.config(state=tk.DISABLED)  # 사용자가 수정하지 못하도록 비활성화 상태로 설정

# GUI 실행
root.mainloop()  # GUI 이벤트 루프 실행 (윈도우 창이 닫힐 때까지 실행됨)
