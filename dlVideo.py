import bs4
import requests
import pafy
from bs4 import BeautifulSoup

def get_search_url(keywords):
    search_url = "https://www.youtube.com/results?q="
    cc_filter = "&sp=EgIwAVAU"

    for keyword in keywords:
        search_url = search_url + keyword
        if keyword is not keywords[len(keywords)-1]:
            search_url = search_url + "+"
    search_url =  search_url + cc_filter
    print(search_url)
    return search_url

def get_download_metadata(url, save_path):
    youtube = pafy.new(url)
    author = youtube.author

    video = youtube.getbest(preftype="mp4")
    video.download(quiet= False,filepath=save_path)

    cc_reference = str("%s: %s" %(author, url))
    #print(cc_reference)
    return cc_reference

def get_video_links(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    a_tags = soup.find_all('a')

    links = []
    for link in a_tags:
        if link['href'].startswith('/watch'):
            links.append(link['href'])
    print(links)
    return links
