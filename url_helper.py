from urllib.request import Request, urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os

def get_url_root(url):
    '''Get the root URL from some URL'''
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if(result == ":///"):
        return None
    return result

def get_href_url(site, href):
    '''Get the full URL for some href (be it a full link or a half link)'''
    root = get_url_root(site)
    if(get_url_root(href) == None):
        href = root + href
    return href

def download_document(document_url, file_name):
    '''Download a document
    
    Example:
    - download_document("https://www.alabamapublichealth.gov/index.html", "publications/assets/organizationalchart.pdf")

    Parameters:
    - document_url -- link to document
    - file_name -- name to save document under
    '''
    response = urlopen(document_url)
    file = open(file_name, 'wb')
    file.write(response.read())
    file.close()

def remove_protocol(url):
    '''Remove "https//www." from the beginning og the link. Fix this ugliness.'''
    if(url.find("https://www.") == 0):
        return url[12:-1]
    if(url.find("http://www.") == 0):
        return url[11:-1]
    if(url.find("https://") == 0):
        url = url[8:-1]
    if(url.find("http://") == 0):
        url = url[7:-1]
    if(url.find("www.") == 0):
        url = url[4:-1]
    if(url.find("//") == 0):
        url = url[2:-1]
    return url

def create_request(url):
    '''Returns a request with specific header information for fetching data from a URL'''
    request = Request(url)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15')
    request.add_header('Accept-Language', 'en-gb')
    request.add_header('Referer', 'https://www.cdc.gov/publichealthgateway/healthdirectories/healthdepartments.html')
    return request

def get_soup_from(address):
    '''
    Returns a BeautifulSoup object from the contents at this address

    Example:
    - get_soup_from("https://ready.alaska.gov/covid19")
    - get_soup_from(HD_PATH + "Alabama Department of Public Health.html")

    Parameters:
    - address -- a file or url
    '''
    if(get_url_root(address) == None):
        if os.path.isfile(address):
            return BeautifulSoup(open(address, errors='ignore'), "html.parser")
        else:
            return None
    try:
        response = urlopen(create_request(address))

        charset = response.headers.get_content_charset()
        if charset == None:
            charset = 'utf-8'

        content = response.read().decode(charset)
        return BeautifulSoup(content, 'html.parser')
    except:
        return None  

#print(get_soup_from(HD_PATH + "Alabama Department of Public Health.html").title)
#print(get_soup_from("https://ready.alaska.gov/covid19").title)