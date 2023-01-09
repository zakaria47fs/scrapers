from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DataObject(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    primary_category: str
    sub_category: str
    product_title: str
    product_brand: str
    old_price: str
    new_price: str
    link_url: str
    thumbnail: str
    description: str
    expiry_date: Optional[str]
    discount_percent: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class DataCategory(BaseModel):
    primary_category: str


class UserCategory(BaseModel):
    categories: List[str]


class UserKeywords(BaseModel):
    keywords: str


class MovieCertificatesObject(BaseModel):
    US: Optional[list]


class MovieDataObject(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titleId: str
    releaseDate: str
    imageUrl: Optional[str]
    runningTimeInMinutes: Optional[str]
    title: Optional[str]
    titleType: Optional[str]
    certificates: Optional[MovieCertificatesObject]
    genres: Optional[list]
    plotOutlineId: Optional[str]
    plotOutlineText: Optional[str]
    plotSummaryId: Optional[str]
    plotSummaryText: Optional[str]
    plotSummaryAuthor: Optional[str]
    videoUrl: Optional[str]
    videoDescription: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

