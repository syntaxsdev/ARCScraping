class User:
    def __init__(self, name, institution):
        self.name = name
        self.institution = institution
        self.research_focus:list = []
        self.research_fields:list = []
        self.expertise:list = []
        self.awards:list = []
        self.appointments:list = []
        '''
        Add objects for other compiled pieces of data
        '''
