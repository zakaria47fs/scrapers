from datetime import datetime


class Movie:
    def __init__(self, titleId, releaseDate, imageUrl=None, runningTimeInMinutes=None, title=None, titleType=None,
                certificates=None, genres=None, plotOutlineId=None, plotOutlineText=None, plotSummaryId=None, plotSummaryText=None,
                plotSummaryAuthor=None, videoUrl=None, videoDescription=None) -> None:
        self.titleId = titleId
        self.releaseDate = releaseDate
        self.imageUrl = imageUrl
        self.runningTimeInMinutes = runningTimeInMinutes
        self.title = title
        self.titleType = titleType
        self.certificates = certificates
        self.genres = genres
        self.plotOutlineId = plotOutlineId
        self.plotOutlineText = plotOutlineText
        self.plotSummaryId = plotSummaryId
        self.plotSummaryText = plotSummaryText
        self.plotSummaryAuthor = plotSummaryAuthor
        self.videoUrl = videoUrl
        self.videoDescription = videoDescription
        self.created_at = datetime.now()

    def data(self):
        return self.__dict__