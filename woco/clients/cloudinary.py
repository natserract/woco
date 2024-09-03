import logging
from typing import Literal, Tuple, Union
import cloudinary
import cloudinary.api
import woco.config as cfg

logger = logging.getLogger(__name__)

class Cloudinary:
    def __init__(self) -> None:
        config = cloudinary.config(
            cloud_name=cfg.CLOUDINARY_CLOUD_NAME,
            api_key=cfg.CLOUDINARY_API_KEY,
            api_secret=cfg.CLOUDINARY_API_SECRET,
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
