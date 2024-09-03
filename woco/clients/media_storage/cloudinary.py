import logging
import cloudinary
import cloudinary.api

from typing import Literal, Tuple, Union
from woco.config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET
)
from woco.clients.media_storage.base import MediaStorage

logger = logging.getLogger(__name__)

class Cloudinary(MediaStorage):
    def __init__(self) -> None:
        config = cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
        )

    def get_assets(
        self,
        dir: str,
        sort_by: Tuple[str, Literal['asc', 'desc']] = ('uploaded_at', 'asc'),
        max_results = 2,
        excludes: list[str] = [] # filename
    ):
        results: list[dict] = []

        try:
            response = cloudinary.Search()\
                .expression(f'folder:{dir}')\
                .sort_by(sort_by[0], sort_by[1])\
                .max_results(max_results)\
                .execute()
            data: list[dict] | None = response.get('resources')
            if data:
                logger.debug(f"Results: {len(data)}")
                for item in data:
                    if item['filename'] not in excludes:
                        results.append(item)

            return results
        except Exception as ex:
            logger.exception(f"Failed to get assets. {ex}")
            raise ValueError(str(ex))
