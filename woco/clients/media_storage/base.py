from abc import ABC, abstractmethod
from typing import Literal, Tuple, Union

class MediaStorage(ABC):
    @abstractmethod
    def get_assets(
        self,
        dir: str,
        sort_by: Tuple[str, Literal['asc', 'desc']] = ('uploaded_at', 'asc'),
        max_results = 2,
        excludes: list[str] = [] # filename
    ) -> list[dict]:
        raise NotImplementedError
