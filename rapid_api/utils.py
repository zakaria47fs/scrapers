import requests


headers = {
	"X-RapidAPI-Key": "cbd430dda1mshdd55098ba37c2c2p148de6jsn046f5815a484",
	"X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
}

om_endpoints = {
    "get-coming-soon-movies": "https://online-movie-database.p.rapidapi.com/title/get-coming-soon-movies",
    "get-overview-details": "https://online-movie-database.p.rapidapi.com/title/get-overview-details",
    "get-videos": "https://online-movie-database.p.rapidapi.com/title/get-videos",
    "get-video-playback": "https://online-movie-database.p.rapidapi.com/title/get-video-playback"
}


def get_movie_details(title_id):
    querystring = {"tconst": title_id, "currentCountry":"US"}
    response = requests.request("GET", om_endpoints['get-overview-details'], headers=headers, params=querystring)
    return response.json()

def get_video_url(video_id):
    querystring = {"viconst": video_id}
    response = requests.request("GET", om_endpoints['get-video-playback'], headers=headers, params=querystring)
    video_urls = [item['playUrl'] for item in response.json().get('resource').get('encodings') if item['definition']=='SD']
    if video_urls:
        return video_urls[0]
    return ''

def movie_video(title_id):
    querystring = {"tconst": title_id,"limit":"25","region":"US"}
    response = requests.request("GET", om_endpoints['get-videos'], headers=headers, params=querystring)
    title_videos = response.json().get('resource').get('videos', [])
    for video in title_videos:
        if video['contentType']=='Trailer':
            return video
    if title_videos:
        return title_videos[0]
    return ''

def get_coming_movies():
    querystring = {"currentCountry":"US","purchaseCountry":"US","homeCountry":"US"}
    response = requests.request("GET", om_endpoints['get-coming-soon-movies'], headers=headers, params=querystring)
    return response.json()