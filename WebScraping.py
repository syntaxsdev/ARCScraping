import requests, random, Universities
from urllib.parse import urlparse
from UserAgents import UserAgents
from User import User
from bs4 import BeautifulSoup

class WebScraping:
    bs4 = None
    def __init__(self):
        self.linkFilterPrefixes = ["/search", "q=", "/?", "/advanced_search"]
        bs4 = BeautifulSoup()

    '''
    The initial search perform a google search on the user using the query "{FIRST LAST} {INSTITUTION}"
    and returns all the links
    '''
    def initial_search(self, user: User):
        user_name = "+".join(user.name) + f" {user.institution}"

        # Tweaks should be done here, maybe make a link scraper by itself

        #search_url = f"https://www.google.com/search?q=%22{user_name}%22"
        search_url = f"https://www.google.com/search?q={user_name}"

        # End of tweaks
        req = self.request(search_url)
        bs = BeautifulSoup(req.content, 'html.parser')

        # Select every single <a> element
        raw_links = bs.select("a")
        # Filter links that do not contain "google.com" or start with the prefixes defined.
        links = [link['href'] for link in raw_links if not any(link['href'].startswith(prefix) 
                    or link['href'].find('google.com') > 0 for prefix in self.linkFilterPrefixes)] 
        
        # Only grab the relevent part of the link if it includes more in it
        links = [link.split("/url?q=")[-1].split("&sa")[0] for link in links]
        user.initial_search_links = links
        return links
    
    '''
    Verify if the link is relevent to the researcher. 2/3 is required to be used.
    1. First checks if the institution can be found on the page text.
    2. Checks if the researchers name can be found on the page check.
    3. Check if the URL is from their institution.
    '''
    def verify_link_relevancy(self, link: str, page_data: str, user: User):
        page_data = page_data.lower()
        user_name = "+".join(user.name).lower()
        checks = 0
        reason = ""

        # Check 1
        if page_data.find(user.institution.lower()):
            checks += 1
            reason += "Instituion found | "

        # Check 2
        if page_data.find(user_name):
            checks += 1
            reason += "Researcher name found | "
        
        # Check 3
        if Universities.findUniversityLink(user.institution).find(link) > -1:
            checks += 1
            reason += "University website verified"
        return (checks >= 2, checks, reason)
        
    ''' 
    Scrape the webpage and get the webtext without HTML tags
    then check verify the source is reputable by a 3 part check method
    '''
    def scrape_webpage(self, link: str, user: User):
        # Request the page and convert to BS4
        req = self.request(link)
        bs = BeautifulSoup(req.content, 'html.parser')
        
        # Grab only the webtext (text without HTML tags)
        webtext = bs.get_text()
        
        # Parse the URL so that we can only get the base domain
        parsed_url = urlparse(link)
        domain_parts = parsed_url.netloc.split('.')
        domain = '.'.join(domain_parts[-2:])

        # Do a 3 part check on the domain, webtext, and the user to verify it pertains to the user
        verified, check, reason = self.verify_link_relevancy(domain, webtext, user)

        # <TODO>
        #NOT DONE
        print(verified, check, reason)
        
    
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
