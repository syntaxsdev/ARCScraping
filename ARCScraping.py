import csv
from WebScraping import WebScraping
from GPT import GPT
from User import User
import pandas as pd
import datetime

'''
The main class that utilizes all of the components to create a full service project
'''
class ARCScraping:

    # Initialize the list of all the researchers we will scrape
    researchers_scraped: list = []

    def __init__(self, file: str):
        # Create the WebScraping object
        self.ws: WebScraping = WebScraping()
        self.GPT: GPT = GPT()

        with open(file, 'r') as file:
            reader = csv.reader(file)
            for researcher in reader:
                user: User = User(researcher[0], researcher[1])
                self.full_scrape(user)

                # After we full_scrape each user, now we must start to export
                self.researchers_scraped.append(user.research_data)

        # Export all scraped researchers
        self.export()


    '''
    Top down scrape of the entire user starting from the initial search engine search
    to the NLP classifications
    '''
    def full_scrape(self, researcher: User) -> User:
        # Get the initial links from the search engine search
        self.ws.initial_search(researcher)

        # Scrape entire researcher from top-down
        self.ws.scrape_researcher(researcher)


    '''
    Export all researchers to a .csv format
    '''
    def export(self):

        for researcher in self.researchers_scraped:
            for key in researcher.keys():
                if (key == "name"):
                    researcher["name"] = ' '.join(researcher["name"])
                else:
                    if (isinstance(researcher[key], list)):
                        if (len(researcher[key]) > 0):
                            if(isinstance(researcher[key][0], dict)):
                                list_dict = User.dedictionaryify(self, researcher[key])
                                researcher[key] = '\n'.join(list_dict)
                            else:
                                researcher[key] = '\n'.join(researcher[key])
                            

        # create a unique filename with timestamp
        export_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        export_filename = f"output_{export_time}.csv"

        df = pd.DataFrame(self.researchers_scraped)

        # export dataframe as .csv file
        df.to_csv(export_filename, index=False)





    