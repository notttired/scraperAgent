from parsers.base_parser import BaseParser
from parsers.bs4_parser import BS4Parser
from typing import List

class ParserManager:
    def __init__(self, important_tags: List[str], content_tags: List[str]):
        self.important_tags = important_tags
        self.content_tags = content_tags

    def get_parser(self) -> BaseParser:
        return BS4Parser(self.important_tags, self.content_tags)
