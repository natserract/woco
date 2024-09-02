import logging
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

    def get_assets_shop(
        self, dir: str, excludes: list[str] = []
    ):
        results: list[dict] = []

        try:
            shop_dir = f'{cfg.ROOT}/upload/shop'
            response = cloudinary.Search()\
                .expression(f'folder:{shop_dir}/{dir}')\
                .sort_by('uploaded_at', 'asc')\
                .max_results(2)\
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
