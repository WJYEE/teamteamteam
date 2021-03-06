# -*- coding: utf-8 -*-
"""11w_crawling_beau_학생1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rbq9W82zLVBLxWmVvwtNJ2NzfVzWdM5n
"""
#학생1 ('네이버영화'라는 사이트에서 영화 순위차트를 크롤링하는 크롤러 코딩)
!pip install beautifulsoup4
!pip install requests

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive')
# %cd /content/drive/MyDrive/Colab Notebooks/11w_crawling/
!pwd
!ls

import requests
from bs4 import BeautifulSoup

url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver'

response = requests.get(url)

if response.status_code == 200:
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  print(soup)
else :
  print(response.status_code)

movies = soup.select('#old_content > table > tbody > tr')

for movie in movies :
  a_rank = movie.select_one('td.ac > img')
  a_tag = movie.select_one('td.title > div > a')
  if a_rank is not None:
    rank, title = a_rank['alt'], a_tag.text
    print(rank,title)
    
#학생 2 (영화차트에서 영화이름을 검색하면 해당 영화의 리뷰를 가져오는 데이터를 크롤링)
import requests
from bs4 import BeautifulSoup

def crawling(soup) :
  result=[]
  ul = soup.find("ul", class_="rvw_list_area")
  for li in ul.find_all("li") :
    result.append(li.find("strong").get_text())
  return result

def get_href(soup) :
  a = soup.find("ul", class_ = "search_list_1").find("a")
  href = a['href'].replace('basic', 'review')
  return "https://movie.naver.com" + href

def get_url(movie) :
  return f"https://movie.naver.com/movie/search/result.nhn?query={movie}&section=all&ie=utf8"

def main():
  list_href = []
  custom_header = {
      'referer' : "https://www.naver.com/",
      'user-agent' : 'Mozilla/5.0 ( Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

  }

  movie = input('영화 제목을 입력하세요. \n > ')

  url = get_url(movie)
  print(url)
  req = requests.get(url, headers = custom_header)
  soup = BeautifulSoup(req.text, "html.parser")

  movie_url = get_href(soup)
  print(movie_url)

  href_req = requests.get(movie_url)
  href_soup = BeautifulSoup(href_req.text, "html.parser")

  list_href = crawling(href_soup)
  print(list_href)


if __name__  == "__main__" :
  main()
