from tqdm import tqdm

from objects import Movie
from utils import get_coming_movies, get_movie_details, movie_video, get_video_url
from services.mongo_service import MongoService


mongo_service = MongoService()
collection_name = 'rapidapi_om_db'

if __name__ == '__main__':
    results = get_coming_movies()
    for res in tqdm(results):
        MovieObj = Movie(titleId=res.get('id').split('/')[-2], releaseDate=res.get('releaseDate'))
        #movie overview details
        movie_details = get_movie_details(title_id=MovieObj.titleId)
        MovieObj.imageUrl = movie_details.get('title').get('image').get('url')
        MovieObj.runningTimeInMinutes = movie_details.get('title').get('runningTimeInMinutes')
        MovieObj.title = movie_details.get('title').get('title')
        MovieObj.titleType = movie_details.get('title').get('titleType')
        MovieObj.certificates = movie_details.get('certificates')
        MovieObj.genres = movie_details.get('genres')
        MovieObj.plotOutlineId = movie_details.get('plotOutline', {}).get('id')
        MovieObj.plotOutlineText = movie_details.get('plotOutline', {}).get('text')
        MovieObj.plotSummaryId = movie_details.get('plotSummary', {}).get('id')
        MovieObj.plotSummaryText = movie_details.get('plotSummary', {}).get('text')
        MovieObj.plotSummaryAuthor = movie_details.get('plotSummary', {}).get('author')
        #movie videos
        video = movie_video(title_id=MovieObj.titleId)
        if video:
            MovieObj.videoDescription = video.get('description', '')
            MovieObj.videoUrl = get_video_url(video_id=video.get('id').split('/')[-1])
        #save to db
        mongo_service.update_by_field(collection_name, 'titleId', MovieObj.data())
