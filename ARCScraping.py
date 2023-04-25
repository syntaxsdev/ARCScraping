import csv, datetime, pandas as pd, asyncio, threading
from WebScraping import WebScraping
from GPT import GPT
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
        self.GPT: GPT = GPT()

        with open(file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for researcher in reader:
                user: User = User(researcher[0], researcher[1])                  
                self.researchers_scraped.append(user)


    '''
    Top down scrape of the entire user starting from the initial search engine search
    to the NLP classifications
    '''
    async def full_scrape(self, researcher: User) -> User:
        print("Begin full scrape")
        # Get the initial links from the search engine search
        self.ws.initial_search(researcher)
        print(f"Researcher [{researcher.research_data['name']}] done with initial search.")
        # Scrape entire researcher from top-down

        print("Ini Links", researcher.initial_search_links)
        await self.ws.scrape_researcher(researcher)
        print(f"Researcher [{researcher.research_data['name']}] done with scraping..")


    def run_async_task(self, async_fn):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(async_fn())
        finally:
            loop.close()

    '''
    Export all researchers to a .csv format
    '''
    def export(self):
        #temp_researchers = self.researchers_scraped.copy()
        researchers_list: list = []
        for researcher in self.researchers_scraped:
            researcher_export_data:dict = {}
            for key, val in researcher.research_data.items():
                dedict: list = researcher.dedictionaryify(val)
                dedict_to_str: str = '\n'.join(dedict)
                    
                researcher_export_data[key] = dedict_to_str
            researchers_list.append(researcher_export_data)


        df = pd.DataFrame(researchers_list)
         # create a unique filename with timestamp
        export_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        export_filename = f"output_{export_time}.xlsx"

        # export dataframe as .csv file
        df.to_excel(export_filename, index=False, engine='openpyxl')


    async def run(self):
        '''
        tasks = [
        asyncio.to_thread(self.full_scrape, researcher)
        for researcher in self.researchers_scraped
        ]
        await asyncio.gather(*tasks)
        '''
        for researcher in self.researchers_scraped:
            await self.full_scrape(researcher)
            #researcher.deduplicate()
        print("Done running all researchers")
        
        self.export()



    