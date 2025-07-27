from loaders.base_loader import BaseLoader
from actions.base_action import BaseAction
from models.navigation_action import NavigationAction

class NavigateTo(BaseAction):
    def __init__(self, action: NavigationAction, loader: BaseLoader):
        super().__init__(action)
        self.loader = loader

    def execute_action(self):
        html_content = self.loader.load(self.action.target)
        return html_content
