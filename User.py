class User:
    def __init__(self, name: str, institution: str):
        self.name = name.split(" ")
        self.institution = institution
        self.research_focus:list = []
        self.research_fields:list = []
        self.expertise:list = []
        self.awards:list = []
        self.appointments:list = []
        self.initial_search_links: list = []
        '''
        Add objects for other compiled pieces of data
        '''
