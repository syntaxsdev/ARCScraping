from fuzzywuzzy import fuzz

class User:
    
    def __init__(self, name: str, institution: str):
        self.research_data: dict = { 
            "name": "",
            "institution": "",
            "gender": "",
            "domain": "",
            "emails": list(),
            "additional_websites": list(),
            "department": list(),
            "research_focus": list(),
            "research_fields": list(),
            "expertise": list(),
            "awards": list(),
            "appointments": list()
        }
        self.research_data['name'] = name.split(" ")
        self.research_data['institution']  = institution
        self.initial_search_links: list = []

    '''
    This method takes all of the possible formats such as dictionaries, 
    etc and shrinks them down into a string list
    '''
    def dedictionaryify(self, field_data):
        newlist = []

        if (type(field_data) == str):
            newlist.append(field_data)
            return newlist
        
        for aw in field_data:
            if (type(aw)==dict):
                newlist.append(' '.join(str(value) for value in aw.values()))
            elif (type(aw)==list):
                # Recursion here
                newlist.extend(self.dedictionaryify(aw)) 
            else:
                if aw != "N/A": 
                    newlist.append(aw)
        return newlist
            
    def is_content_similar(self, name1, name2, threshold=85):
        similarity = fuzz.token_set_ratio(name1, name2)
        return similarity >= threshold

    def deduplicate(self, threshold=85):
        fields = self.research_data
        deduplicated_fields = {}

        for key, values in fields.items():
            unique_vals = []
            for value in values:
                if not any(self.is_content_similar(value, unique_val, threshold) for unique_val in unique_vals):
                    unique_vals.append(value)
            deduplicated_fields[key] = unique_vals
            
        self.research_data = deduplicated_fields
