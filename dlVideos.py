import bs4
import requests
import pafy
from bs4 import BeautifulSoup
import random

def get_search_url(keywords):
    search_url = "https://www.youtube.com/results?q="
    cc_filter = "&sp=EgIwAVAU"

    for keyword in keywords:
        search_url = search_url + keyword
        if keyword is not keywords[len(keywords)-1]:
            search_url = search_url + "+"
    search_url =  search_url + cc_filter
    print("search url:\t"+search_url)
    return search_url

def get_video_links(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    a_tags = soup.find_all('a')

    all_ids = []
    for link in a_tags:
        if link['href'].startswith('/watch'):
            ytid = link['href'].replace('/watch?v=','')
            all_ids.append(ytid)
    #print(len(all_ids))
    return all_ids

def get_download_metadata(link, save_path):
    url = "https://www.youtube.com/watch?v=" + link
    print(url)
    youtube = pafy.new(link)
    author = youtube.author

    # download vdeo in best available mp4-format
    minLength = 2
    maxLength = 15
    duration = youtube.duration.split(':')
    if int(duration[0]) < 1 and int(duration[1]) < 15:
        video = youtube.getbest(preftype="mp4")
        video.download(quiet= False,filepath=save_path)
    else:
        raise ValueError('Video doesn\'t fit!')

    cc_reference = str("%s: %s" %(author, url)) # store creative commons author and link to original video
    # print("%s saved to: %s" %(video.title, save_path))
    # print(cc_reference)
    return cc_reference

def save_metadata_txt(save_path,all_metadata):
    with open(save_path+"cc_authors.txt", "w", newline="\r\n") as o:
        for metadata in all_metadata:
            o.write(metadata+"\n")

def downloadVideos(keywords, save_path, shrink):
    search_url = get_search_url(keywords)
    links = get_video_links(search_url) # get all /watch[*]- links

    #take unvisited, random link, try to download and set metadata
    all_metadata = []
    visited = []
    while shrink:
        link = random.choice(links)
        if link not in visited:
            visited.append(link)
            try:
                metadata = get_download_metadata(link, save_path)
                all_metadata.append(metadata)
                shrink = shrink - 1
            except Exception as e:
                pass


    save_metadata_txt(save_path, all_metadata) # save cc_authors.txt in SAVE_PATH
