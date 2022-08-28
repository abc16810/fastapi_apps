from dataclasses import dataclass, field
from fastapi import Body, UploadFile, File, HTTPException
import re
from types import DynamicClassAttribute
from typing import Dict
from enum import Enum


ALLOW_MEDIA_TYPE = {'image/tiff; application=geotiff': 'tif', 'image/png': 'png',  'text/plain': 'txt',
                    'application/x-zip-compressed':'zip'}


class MediaType(str, Enum):
    """Responses Media types formerly known as MIME types."""

    tif = "image/tiff; application=geotiff"
    jp2 = "image/jp2"
    png = "image/png"
    pngraw = "image/png"
    jpeg = "image/jpeg"
    jpg = "image/jpg"
    webp = "image/webp"
    npy = "application/x-binary"
    xml = "application/xml"
    json = "application/json"
    geojson = "application/geo+json"
    html = "text/html"
    txt = "text/plain"
    pbf = "application/x-protobuf"
    mvt = "application/x-protobuf"
    zip = "application/x-zip-compressed"
    csv = "application/vnd.ms-excel"


class DataFormat(str, Enum):
    """Data Format Base Class."""

    @DynamicClassAttribute
    def mediatype(self):
        """Return image mimetype."""
        return MediaType[self._name_].value


class RasterFormat(DataFormat):
    """Available Input format."""

    text = "text"
    png = "png"


# @dataclass
# class DefaultDependency:
#     """"""
#
#     def keys(self):
#         """Return Keys."""
#         return self.__dict__.keys()
#
#     def __getitem__(self, key):
#         """Return value."""
#         return self.__dict__[key]


@dataclass
class DefaultDependency:
    kwargs: Dict = field(default_factory=dict, init=False)  # 其它参数 默认{}


@dataclass
class UploadFileParam(DefaultDependency):
    """file upload parameters."""

    identifier: str = Body(
        ..., title="identifier", description="文件唯一标识符"
    )
    number: str = Body(
        ..., title="number ", description="文件分片序号", max_length=2)
    file: UploadFile = File(..., description='文件')

    def __post_init__(self):
        """post init"""
        identifier = self.identifier
        file = self.file
        res = re.match('\w+', identifier)
        if not res or res.group() != identifier:
            raise HTTPException(detail="Invalid identifier", status_code=200)
        if file.content_type not in ALLOW_MEDIA_TYPE.keys():
            raise HTTPException(detail="Invalid media type", status_code=200)
        else:
            self.kwargs['prefix'] = ALLOW_MEDIA_TYPE.get(file.content_type)



