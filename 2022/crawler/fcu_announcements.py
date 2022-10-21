import requests
from bs4 import BeautifulSoup

# 使用requests發送get請求給指定網址
response = requests.get(
    "https://www.fcu.edu.tw/announcements/")
# 將HTML印出
print(response.text)

# html.parser為Python內建的HTML解析器
soup = BeautifulSoup(response.text, "html.parser")

# 抓取全部class為a-news-list__main的元素
news_list = soup.find_all(class_="a-news-list__main")

# 遍歷每一個元素, 並印出相關資料
for news in news_list:
    # 抓取特定元素內的文字
    date = news.find(class_="a-news-list__date").text
    # 將多餘的空格去除
    date = date.strip()

    category = news.find(class_="a-news-list__category").text
    unit = news.find(class_="a-news-list__unit").span.text  # 公告單位被span包著

    title_element = news.find(class_="a-news-list__title")
    title = title_element.text
    url = title_element.get("href")  # 抓取元素的href屬性

    print(date, category, unit, title, sep=" | ")