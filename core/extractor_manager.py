from extractors.bs4_extractor import BS4Extractor
from typing import List

class ExtractorManager:
    def __init__(self, important_tags: List[str], content_tags: List[str]):
        self.important_tags = important_tags
        self.content_tags = content_tags

    def get_extractor(self):
        return BS4Extractor(self.important_tags, self.content_tags)
