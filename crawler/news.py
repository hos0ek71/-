import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import time

# 뉴스 검색 API 호출 함수
def get_news(query, client_id, client_secret, display=10, start=1):
    url = 'https://openapi.naver.com/v1/search/news.json'
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': 'date'
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        return []

# 뉴스 크롤링 결과를 출력하는 함수
def display_news(news_items):
    result_box.config(state=tk.NORMAL)
    result_box.delete(1.0, tk.END)
    for item in news_items:
        title = item['title']
        originallink = item['originallink']
        link = item['link']
        description = item['description']
        pub_date = item['pubDate']

        result_box.insert(tk.END, f"제목: {title}\n")
        result_box.insert(tk.END, f"원본 링크: {originallink}\n")
        result_box.insert(tk.END, f"네이버 뉴스 링크: {link}\n")
        result_box.insert(tk.END, f"요약: {description}\n")
        result_box.insert(tk.END, f"발행 날짜: {pub_date}\n")
        result_box.insert(tk.END, '-' * 80 + '\n')

    result_box.config(state=tk.DISABLED)

# 뉴스 검색 시작 함수
def search_news():
    keyword = keyword_entry.get()
    total_pages = int(page_entry.get())
    client_id = client_id_entry.get()
    client_secret = client_secret_entry.get()

    if not keyword or not client_id or not client_secret:
        messagebox.showerror("입력 오류", "모든 입력 필드를 채워주세요.")
        return

    result_box.config(state=tk.NORMAL)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"'{keyword}'로 검색 중...\n")
    result_box.config(state=tk.DISABLED)

    for page in range(1, total_pages + 1):
        news_items = get_news(keyword, client_id, client_secret, display=10, start=(page - 1) * 10 + 1)
        if news_items:
            display_news(news_items)
        else:
            messagebox.showinfo("결과 없음", "검색 결과가 없습니다.")
        if page < total_pages:
            time.sleep(1)  # 1초 딜레이 추가

# Tkinter GUI 구성
root = tk.Tk()
root.title("네이버 뉴스 크롤러")

# Client ID 입력 필드
tk.Label(root, text="Client ID:").grid(row=0, column=0, padx=10, pady=10)
client_id_entry = tk.Entry(root, width=30)
client_id_entry.grid(row=0, column=1, padx=10, pady=10)

# Client Secret 입력 필드
tk.Label(root, text="Client Secret:").grid(row=1, column=0, padx=10, pady=10)
client_secret_entry = tk.Entry(root, width=30, show="*")  # 입력을 가리기 위해 show="*" 추가
client_secret_entry.grid(row=1, column=1, padx=10, pady=10)

# 키워드 입력 필드
tk.Label(root, text="키워드:").grid(row=2, column=0, padx=10, pady=10)
keyword_entry = tk.Entry(root, width=30)
keyword_entry.grid(row=2, column=1, padx=10, pady=10)

# 페이지 수 입력 필드
tk.Label(root, text="페이지 수:").grid(row=3, column=0, padx=10, pady=10)
page_entry = tk.Entry(root, width=30)
page_entry.grid(row=3, column=1, padx=10, pady=10)

# 검색 버튼
search_button = tk.Button(root, text="검색 시작", command=search_news)
search_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# 결과 출력 스크롤 텍스트 박스
result_box = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
result_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
result_box.config(state=tk.DISABLED)

# GUI 실행
root.mainloop()
