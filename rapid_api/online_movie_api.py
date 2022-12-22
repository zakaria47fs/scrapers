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




def get_video_url(video_id):
    querystring = {"viconst": video_id}
    response = requests.request("GET", om_endpoints['get-video-playback'], headers=headers, params=querystring)
    video_urls = [item['playUrl'] for item in response.json().get('resource').get('encodings') if item['definition']=='SD']
    if video_urls:
        return video_urls[0]
    return ''



if __name__=='__main__':
    querystring = {"currentCountry":"US","purchaseCountry":"US","homeCountry":"US"}
    response = requests.request("GET", om_endpoints['get-coming-soon-movies'], headers=headers, params=querystring)
    titles = [{'title_id': title.get('id').split('/')[-2], 'releaseDate': title.get('releaseDate')} for title in response.json()]
    
