import pafy

url = "https://www.youtube.com/watch?v=19WUwZYM7bM"
save_path = "/media/HDDLinux"

def get_download_metadata(url, save_path):
    youtube = pafy.new(url)
    author = youtube.author

    video = youtube.getbest(preftype="mp4")
    video.download(quiet= False,filepath=save_path)

    cc_reference = str("%s: %s" %(author, url))
    #print(cc_reference)
    return cc_reference
