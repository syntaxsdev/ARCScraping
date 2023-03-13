import csv
from WebScraping import WebScraping
from User import User

'''
The main class that utilizes all of the components to create a full service project
'''
class ARCScraping:

    # Initialize the list of all the researchers we will scrape
    researchers_scraped: list = []

    def __init__(self, file: str):
        # Create the WebScraping object
        self.ws: WebScraping = WebScraping()


        with open(file, 'r') as file:
            reader = csv.reader(file)
            for researcher in reader:
                user: User = User(researcher[0], researcher[1])
                self.full_scrape(user)
                
                # After we full_scrape each user, now we must start to export
                self.researchers_scraped.append(user)

        # Export all scraped researchers
        export_name = file.strip(".")[0] + "_exported.csv"
        self.export(export_name)


    '''
    Top down scrape of the entire user starting from the initial search engine search
    to the NLP classifications
    '''
    def full_scrape(self, researcher: User) -> User:
        # Get the initial links from the search engine search
        self.ws.initial_search(researcher)

        # Scrape each webpage from the initial_search
        for initial_search in researcher.initial_search_links:
            self.ws.scrape_webpage(initial_search, researcher)

        #<TODO> NOT DONE
        #.....


    '''
    Export all researchers to a .csv format
    '''
    def export(self, export_name):
        pass


    