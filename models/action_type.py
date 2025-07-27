from enum import Enum

class ActionType(Enum):
    CLICK = "click"
    SCROLL = "scroll"
    EXTRACT = "extract"
    SEARCH_PAGE = "search_page"
    NAVIGATE_TO = "navigate_to"
    COMPLETE = "complete"
