class User:
    
    def __init__(self, name: str, institution: str):
        self.research_data: dict = { 
            "name": "",
            "institution": "",
            "email": "",
            "gender": "",
            "department": "",
            "domain": "",
            "additional_websites": list(),
            "research_focus": list(),
            "research_fields": list(),
            "expertise": list(),
            "awards": list(),
            "appointments": list()
        }
        self.research_data['name'] = name.split(" ")
        self.research_data['institution']  = institution
        self.initial_search_links: list = []

        def scrape_data(data: dict):
            '''
            Append all scraped data to list
            '''
            self.research_fields.append(data['research_fields'])
            self.research_focus.append(data['research_focus'])
            self.expertise.append(data['expertise'])
            if (type(data['awards']) == list):
                for award in data['awards']:
                    self.awards.append(award)
            else:
                self.awards.append(data['awards'])

             