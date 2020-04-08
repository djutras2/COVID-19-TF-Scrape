from urllib.request import Request, urlopen
import urllib
import shutil
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlparse

# url = "ftp://rockyftp.cr.usgs.gov/"

# soup = BeautifulSoup(url, "html.parser")

# for a in soup.select("td a"): # <td data-value="s14w171/"><a class="icon dir" href="ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1/TIFF/s14w171/">s14w171/</a></td>
#     title = a.string[0:-1]
#     print(a.string[0:-1])
#     url = a.get("href") + "USGS_1_" + title + ".tif"
#     # print(url)
#     file_name = "C:/Users/RDAGCDLJ/Documents/FY20/GeoTIFF/example_tiffs/USGS_1/" + title + ".tif"
#     #print(file_name)

#     with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
#         shutil.copyfileobj(response, out_file)

"""
TODO

gather list of health department websites (https://www.cdc.gov/publichealthgateway/healthdirectories/healthdepartments.html)

parse links

save html locally for testing - done

parse local html for COVID links and files

implement for real-time, daily update capabalities

"""

HD_PATH = "State HD Sites/"

failed = [('Arkansas Department of Health', 'http://www.healthy.arkansas.gov/Pages/default.aspx')]

def get_url_root(url):
    '''Get the root URL from some URL'''
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if(result == ":///"):
        return None
    return result

# print(get_url_root("https://www.alabamapublichealth.gov/index.html"))
# print(get_url_root("publications/assets/organizationalchart.pdf"))
# print(get_url_root("https://www.alabamapublichealth.gov/calendar/2019/07/hwi-training.html"))
# print(get_url_root("legal/public-health-laws.html"))

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

'''Extracts all health department info from the CDC website'''
def extract_hds():
    soup = BeautifulSoup(open("./State and Territorial Health Department Websites.html"), "html.parser")
    urls = []
    names = []
    for a in soup.select("a"):
        urls.append(a.get("href"))
        names.append(a.contents[0])
    return names, urls

hds = extract_hds()

def save_hd_urls():
    hds = extract_hds()
    with open("hd_list", "w") as hd_list:
        for name, url in zip(hds[0], hds[1]):
            if not name == None and not url == None:
                hd_list.write(name + "\t" + url)

def save_html_locally(name, url):
    print("Trying " + name)
    try:
        # fetch content
        response = urlopen(create_request(url))

        charset = response.headers.get_content_charset()
        if charset == None:
            charset = 'utf-8'

        content = response.read().decode(charset)

        # save site
        with open(HD_PATH + name + ".html", 'w', encoding=charset) as out_file:
            if(content == None):
                return False
            #shutil.copyfileobj(content, out_file)
            out_file.write(content)
            return True
    except urllib.error.HTTPError:
        print("Error: httpError")
        return False
    except RuntimeError as e:
        print("Error: " + e)
        return False

def save_all_html_locally(names, urls, to_do = None):
    failures = []
    for name, url in zip(names, urls):
        if not name == None and not url == None:
            if(to_do == None or any(name.split(" ")[0] in hd_tuple[0] for hd_tuple in to_do)):
                success = save_html_locally(name, url)
                if(not success):
                    print(name + " failed to save")
                    failures.append((name, url))
    print("Failures:")
    print(failures)
    return failures

### extract all html to local folder

# failed = [('Arkansas Department of Health', 'http://www.healthy.arkansas.gov/Pages/default.aspx')]
# save_all_html_locally(hds[0], hds[1], failed)

'''Get the full URL for some href (be it a full link or a half link)'''
def get_href_url(site, href):
    root = get_url_root(site)
    if(get_url_root(href) == None):
        href = root + href
    return href

'''Download a document'''
def download_document(document_url):
    response = urlopen(document_url)
    file = open(document_url, 'wb')
    file.write(response.read())
    file.close()

# download_document("https://www.alabamapublichealth.gov/index.html", "publications/assets/organizationalchart.pdf")

# remove "https//www."" from the beginning og the link. Fix this.
def remove_protocol(url):
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

'''
(Recursively) Parse an address for COVID/coronavirus links and files
    address - website or file
    link - optional arg for when the address is a filename
'''

stop_words = ["guidance", "unemployment", "school", "disabilit", "financial", "you", "homemade", "yourself", "cdc.gov", "masks", "whitehouse.gov", "cloth", "face", "faq", "education", "recommendations", "emotional", "videos", "providers"]
search_words = ["data", "map", "update", "daily", "zip_code", "zip-code", "zipcode", "code", "numbers", "analysis"]
wms_words = ["tableau", "gis", "mapbox", "esri"]

def parse_for_covid(address, url=None, state=None, site_limit = 50, info=None):
    '''
    Recursively parses an address for COVID/coronavirus links and files. Returns relevant info.
    
    Example:
    - print_parse_for_covid(HD_PATH + "Oregon Health Authority, Public Health Division.html", "https://www.oregon.gov/oha/ph/pages/index.aspx", state="Oregon", site_limit=50)

    Parameters:
    - address -- a file or url
    - url -- url for visiting site references
    - state -- state that is being searched (will ensure visited sites are relevant to this state)
    - site-limit -- max number of sites to visit
    - info -- for recursing, carries information about findings and sites visited
            - info[0] = visited sites
            - info[1] = promising sites
            - info[2] = promising downloads
            - info[3] = WMSs?
    '''
    if(info == None):
        info = []
        for i in range(4):
            info.append([]) # three lists, each holding info

    # track visited sites
    #visited_sites = previously_visited_sites
    if(url == None):
        url = address
    info[0].append(remove_protocol(url)) # visited sites

    try:
        # fetch soup for this address
        soup = get_soup_from(address)
        if(soup == None):
            # print("Invalid address: " + address)
            return info

        # eliminate unrelated addresses
        if(state != None and not (state.lower() in soup.getText().lower())):
            #print("This address is not affiliated with " + state + ": " + address)
            return info

        # print("Trying: " + address)

        info[1].append(address) # promising sites

        for tag in soup.find_all("a", href=re.compile("COVID|coronavirus")):
            # get address
            href = tag.get('href')
            href_lower = tag.get('href').lower()

            # FILTER
            if("mailto:" in href_lower):
                continue

            if(any(x in href_lower for x in stop_words)):
                # print("This address is unlikely to be helpful: "  + href)
                continue

            # check if this site has already been visited
            if(remove_protocol(get_href_url(url, href)) in info[0]):
                # print("This address has already been visited: " + href)
                continue

            #print("Looking at: " + get_href_url(url, href))

            # GET FILES
            if(href_lower.endswith(".pdf") or href_lower.endswith(".json") or href_lower.endswith(".csv")):
                #document_url(get_href_url(link, tag.get('href')))
                if(any(x in href_lower for x in search_words)):
                    info[2].append(get_href_url(url, href)) # promising downloads
                #else:
                    #print("\t-Potential, but skipping.")

                info[0].append(remove_protocol(get_href_url(url, href))) # visited sites
                continue

            # GET WMSs
            if(any(x in href_lower for x in wms_words)):
                info[3].append(get_href_url(url, href)) # potential wms

            # RECURSE
            if(len(info[0]) < site_limit):
                info = parse_for_covid(get_href_url(url, href), state=state, info=info)

            # if("map" in href_lower):
            #     #document_url(get_href_url(link, tag.get('href')))
            #     print("Potential for map: " + get_href_url(url, href))
            #     info = parse_for_covid(get_href_url(url, href), state=state, info=info)

    except UnicodeDecodeError as e:
        print(e)
    return info

def print_parse_for_covid(address, url=None, state=None, site_limit = 50):
    info = parse_for_covid(address, url, state, site_limit)
    if(state==None):
        state = ""
    print("\n%s Results:\n\nAll Visited Sites\n%a\nRelated Sites:\n%a\nPotential Files for Download:\n%a\nPotential Web Mapping Services:\n%a\n" %(state, info[0], info[1], info[2], info[3]))

# for filename in os.listdir(HD_PATH):
#     try:
#         soup = BeautifulSoup(open(os.path.join(HD_PATH, filename), 'r'), "html.parser")
#         print(soup.title)
#     except  e:
#         print(e)



#parse_for_covid(HD_PATH + "Alabama Department of Public Health.html", "https://www.alabamapublichealth.gov/index.html")
#parse_for_covid(HD_PATH + "Alabama Department of Public Health.html", "https://www.alabamapublichealth.gov/index.html")

#print_parse_for_covid(HD_PATH + "South Carolina Department of Health and Environmental Control.html", "https://www.scdhec.gov/", state="South Carolina", site_limit=100)

test_addresses = [("Alabama Department of Public Health.html", "https://www.alabamapublichealth.gov/index.html"), "https://www.oregon.gov/oha/ph/pages/index.aspx"]

def parse_all_for_covid(addresses):
    for address in addresses:
        if address != None:
            if(type(address) == tuple):
                print(address[0] + ", " + address[1])
                #parse_for_covid(address[0], address[1])
            else:
                print(address)
                # parse_for_covid(name)


def main():
    print_parse_for_covid(HD_PATH + "Oregon Health Authority, Public Health Division.html", "https://www.oregon.gov/oha/ph/pages/index.aspx", state="Oregon", site_limit=50)

if __name__ == "__main__":
    main()


# Look into this:
# http://www.healthdata.org/covid/data-downloads