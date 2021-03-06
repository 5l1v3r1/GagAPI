import requests
import json
import re

from BeautifulSoup import BeautifulSoup as bs

BASE_URL = "https://9gag.com"

PAGE_DICT = {
  'hot' : '/hot',
  'trending' : '/trending',
  'fresh' : '/fresh',
  'nsfw' : '/nsfw',
  'cute' : '/cute',
  'geeky': '/geeky',
  'meme' : '/meme',
  'cute' : '/cosplay',
  'comic': '/comic',
  'cosplay': '/cosplay',
  'timely': '/timely',
  'wtf' : '/wtf',
  'girl': '/girl',
  'fresh' : '/fresh' 
  }
def get_page(page_url = ""):
  try:
    #Solved the inifnite scrolling problem.
    content = requests.get("%s%s" %(BASE_URL, page_url)).text
    return bs(content)
  except:
    return None

def retrieve_articles(number_of_pages, page_type):
  extend_url = ""
  if page_type != None:
    try:
      extend_url = PAGE_DICT[page_type]
    except:
      extenf_url = ""
  print extend_url
  all_articles = list()
  while number_of_pages > 0:
    content = get_page(extend_url)
    if content == None:
      return None
    extend_url = content.find('a', attrs={'class' : 'btn badge-load-more-post'})['href']
    #print extend_url
    all_articles += content.findAll("article")
    number_of_pages -= 1
    #print all_articles[0]
  return all_articles

#Add filters such that the user can go ahead and limit whether
#they want only gifs, images, posts with comments above this number,#posts with comments greater than 
#Make sure that the page number limit is 100. 
 
def annotate(number_of_pages, page_type):
  final_result = list()
  for ii in retrieve_articles(number_of_pages, page_type):
    #TODO : Make the dictionary by getting other elements out. 
    try:
      type = ii.find('span', attrs = {'class' : 'play badge-gif-play hide'}).text
      media_url = ii.find('img', attrs = {'class' : 'badge-item-animated-img'})['src'] 
    except:
      type = 'Image'
      media_url = ii.find('img', attrs = {'class' : 'badge-item-img'})['src']
    post_url = ii['data-entry-url']
    votes = ii['data-entry-votes']
    comments = ii['data-entry-comments']
    title = ii.find('img', attrs={'class':'badge-item-img'})['alt'] 
    #print title
    final_result.append({
      "type" : type , 
      "post_url" : post_url,
      "votes" : int(votes),
      "comments" : int(comments),
      "title" : title,
      "media_url" : media_url
    })
  return final_result

def get_posts_from_page(number_of_pages = 1, media_type = 'all', page_type = None, more_votes_than = 0, more_comments_than = 0):
  data = annotate(number_of_pages, page_type)
  if media_type == 'gif':
    data = [el for el in data if el['type'] == 'GIF']
  elif media_type == 'image':
    data = [el for el in data if el['type'] == 'Image']
  else:
    pass 
  if more_votes_than > 0:
    data = [el for el in data if el['votes'] > more_votes_than]
  if more_comments_than > 0:
    data = [el for el in data if el['comments'] > more_comments_than]
  return json.dumps(data)
