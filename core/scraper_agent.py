from core.loader_manager import LoaderManager

important_tags = ['a', 'button', 'input', 'select', 'textarea', 'form', 'nav', 'menu', 'img']
content_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'section', 'article']
concurrency_limit = 10

class BaseScraper:
    def __init__(self):
        self.loader_manager = LoaderManager()
        self.scraper = StructuredScraper()
        self.extractors = ExtractorManager()
        self.navigator = NavigationController()

    def run(self):
        while not self.navigator.should_stop():
            html = self.scraper.load_page()
            extracted = self.extractors.extract(html)
            action = self.navigator.decide_next_action(extracted)
            self.scraper.execute_action(action)
