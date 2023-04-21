import requests, random, Universities, re
from GPT import GPT
from urllib.parse import urlparse
from UserAgents import UserAgents
from User import User
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from threading import Thread
import difflib


class WebScraping:
    bs4 = None
    def __init__(self):
        self.linkFilterPrefixes = ["/search", "q=", "/?", "/advanced_search"]
        self.linkFilterSearches = ["google", "facebook", "instagram", "linkedin", "twitter", "ratemyprofessors",
                                   "coursicle", "youtube"]
        bs4 = BeautifulSoup()
        self.GPT = GPT()

    '''
    The initial search perform a google search on the user using the query "{FIRST LAST} {INSTITUTION}"
    and returns all the links
    '''
    def initial_search(self, user: User):
        # user_name = "+".join(user.research_data['name']) + f" {user.research_data['institution']}"

        # # Tweaks should be done here, maybe make a link scraper by itself

        # #search_url = f"https://www.google.com/search?q=%22{user_name}%22"
        # search_url = f"https://www.google.com/search?q={user_name}"

        # # End of tweaks
        # req = self.request(search_url)
        # bs = BeautifulSoup(req.content, 'html.parser')

        # # Select every single <a> element
        # raw_links = bs.select("a")
        # # Filter links that do not contain "google.com" or start with the prefixes defined.
        # links = [link['href'] for link in raw_links if not any(link['href'].startswith(prefix) 
        #             or link['href'].find('google.com') > 0 for prefix in self.linkFilterPrefixes)] 
        
        # # Filter links that don't contain searches
        # links = [link for link in links if not any(link.find(search) > -1 for search in self.linkFilterSearches)]

        # # Only grab the relevent part of the link if it includes more in it
        # links = [link.split("/url?q=")[-1].split("&sa")[0] for link in links]
        # user.initial_search_links = links
        # return links


        user_name = "+".join(user.research_data['name']) + f" {user.research_data['institution']}"
        links = []

        for page_number in range(3):
            start_index = page_number * 10
            search_url = f"https://www.google.com/search?q={user_name}&start={start_index}"

            req = self.request(search_url)
            bs = BeautifulSoup(req.content, 'html.parser')

            # Select every single <a> element
            raw_links = bs.select("a")
            # Filter links that do not contain "google.com" or start with the prefixes defined.
            filtered_links = [link['href'] for link in raw_links if not any(link['href'].startswith(prefix) 
                        or link['href'].find('google.com') > 0 for prefix in self.linkFilterPrefixes)] 
        
            # Filter links that don't contain searches
            filtered_links = [link for link in filtered_links if not any(link.find(search) > -1 for search in self.linkFilterSearches)]

            # Only grab the relevent part of the link if it includes more in it
            links += [link.split("/url?q=")[-1].split("&sa")[0] for link in filtered_links]

        user.initial_search_links = links
        # links = list(set(links))
        return links
    
    '''
    Verify if the link is relevent to the researcher. 2/3 is required to be used.
    1. First checks if the institution can be found on the page text.
    2. Checks if the researchers name can be found on the page check.
    3. Check if the URL is from their institution.
    '''
    def verify_link_relevancy(self, link: str, page_data: str, user: User):
        page_data: str = page_data.lower()
        user_name: str = " ".join(user.research_data['name']).lower()
        checks: int  = 0
        reason: str = ""

        # Check 1
        institution: str = user.research_data['institution']
        if page_data.find(institution.lower()) > -1:
            checks += 1
            reason += "Institution found | "

        # Check 2
        if page_data.find(user_name) > -1 or self.is_name_in_text(user_name, page_data):
            checks += 1
            reason += "Researcher name found | "
        
        # Check 3
        if Universities.findUniversityLink(user.research_data['institution']).find(link) > -1:
            checks += 1
            reason += "University website verified"
        add_prompt: str = f"The researcher: {user_name} | Institution: {institution}"

        return (checks >= 2, checks, reason, add_prompt)
        
    ''' 
    Scrape the webpage and get the webtext without HTML tags
    then check verify the source is reputable by a 3 part check method
    '''
    def scrape_webpage(self, link: str, user: User, checks):
        # Request the page and convert to BS4
        req = self.request(link)
        bs = BeautifulSoup(req.content, 'html.parser')
        
        # Grab only the webtext (text without HTML tags)
        webtext = bs.get_text().replace('\n', '').replace('"', '').strip()
        
        # Parse the URL so that we can only get the base domain
        parsed_url = urlparse(link)
        domain_parts = parsed_url.netloc.split('.')
        domain = '.'.join(domain_parts[-2:])

        # Do a 3 part check on the domain, webtext, and the user to verify it pertains to the user
        verified, check, reason, prompt = self.verify_link_relevancy(domain, webtext, user)

        if check >= checks and verified:
            json_data = self.GPT.scrape(webtext, prompt)
            for json in json_data:
                for key, value in json.items():
                    v_data = str(value)
                    if (key == "name"):
                        continue
                    if (type(value)==list):
                        user.research_data[key].extend(value)
                    else:
                        if (value == 'N/A' or value == None):
                            continue
                        if (type(user.research_data[key])==list):
                            user.research_data[key].append(value)
                        else:
                            user.research_data[key] = value

    '''
    Removes similar values in the scraped
    data and keeps only unique ones
    '''
    def remove_similar_values(self, input_dict, threshold=80):
        for key, value in input_dict.items():
            if isinstance(value, list):
                cleaned_values = []
                for v in value:
                    # Check similarity between current value and previously cleaned values
                    similarity = max([fuzz.token_sort_ratio(v, cleaned_v) for cleaned_v in cleaned_values] + [0])
                    if similarity < threshold:
                        cleaned_values.append(v)
                input_dict[key] = cleaned_values
            else:
                if key not in input_dict:
                    input_dict[key] = value
                else:
                    similarity = fuzz.token_sort_ratio(value, input_dict[key])
                    if similarity < threshold:
                        input_dict[key] = value
        return input_dict

    '''
    Scrape all the webpages from the user
    and implement into their research_data field
    '''
    def scrape_researcher(self, user: User, checks = 2):
        thread_list : list[Thread] = []
        for page in user.initial_search_links:
            # print("[New Scrape]")
            
            # Start threading
            thread = Thread(target=self.scrape_webpage, args=(page, user, checks))
            thread_list.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in thread_list:
            thread.join()
        self.remove_similar_values(user.research_data)

    '''
    Check if names are similar in case of shortened names
    '''
    def is_name_similar(self, name1, name2, threshold=60):
        similarity = fuzz.token_set_ratio(name1, name2)
        return similarity >= threshold


    '''
    Extract all names in the webtext
    '''
    def extract_names(self, text):
        # A simple regex pattern for extracting names with format "FirstName LastName"
        name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
        names = re.findall(name_pattern, text)
        return names


    '''
    Check if name is in the webtext
    '''
    def is_name_in_text(self, name, text, threshold=80):
        names = set(self.extract_names(text))
        for extracted_name in names:
            if fuzz.token_set_ratio(name, extracted_name) >= threshold:
                return True
        return False


    '''
    Internal request method that faciliates parameters and headers
    :return: `Response`
    '''
    def request(self, link) -> requests.Response:
        return requests.get(link, self.genHeaders())

    '''
    Generate new headers
    '''
    def genHeaders(self) -> dict:
        return {
        'User-agent': self.getRandAgent()
        }

    ''' 
    Returns a random UserAgent for the headers
    '''
    def getRandAgent(self) -> str:
        return UserAgents[random.randrange(len(UserAgents))]