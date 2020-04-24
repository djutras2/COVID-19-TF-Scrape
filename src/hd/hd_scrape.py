from urllib.request import Request, urlopen
import urllib
import re
from hd_list_extraction import get_test_hd_tuples, get_hd_tuples
from url_helper import get_href_url, download_document, remove_protocol, get_url_root, create_request
from url_helper2 import get_soup_from
from words import stop_words, search_words, wms_words

import time

"""
Title: hd_scrape.py
Author: Dustin Jutras, AGC
Date: 04/06/20

TODOS?
- nebraska broke, arkansas, etc. Need to handle these cases batter
- optional printing in parse_for_covid
- getting stuff like mapbox.com, need to make sure sites are relevant to the State before deep diving into iframes. Wasting time.
- slowwww
"""

LOGGING = True
HD_PATH = "State HD Sites/" # temp

failed = [('Arkansas Department of Health', 'http://www.healthy.arkansas.gov/Pages/default.aspx')]

# TODO: revisit
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

# TODO: revisit
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


'''
(Recursively) Parse an address for COVID/coronavirus links and files
    address - website or file
    link - optional arg for when the address is a filename
'''

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
        for _ in range(4):
            info.append([]) # three lists, each holding info

    # track visited sites
    #visited_sites = previously_visited_sites
    if(url == None):
        url = address
    info[0].append(remove_protocol(url)) # visited sites

    try:
        # fetch soup for this address
        soup = get_soup_from(address, state) # added require word to try to narrow down search before searching iframes, speed things up
        if(soup == None):
            # print("Invalid address: " + address)
            return info

        # eliminate unrelated addresses, now done in get_soup_from
        # if(state != None and not (state.lower() in soup.getText().lower())):
        #     #print("This address is not affiliated with " + state + ": " + address)
        #     return info

        # print("Trying: " + address)

        info[1].append(address) # promising sites

        # GET WMSs (checks this page for embedded WMSs)
        if(any(x in soup.getText().lower() for x in wms_words)):
            info[3].append(address) # potential wms

        for tag in soup.find_all("a"): #, href=re.compile("COVID|coronavirus|arcgis")):
            # get address
            href = tag.get('href')
            if(href == None):
                continue
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

            # CHECK IS WMS (checks a reference for a potential WMS)
            if(any(x in href_lower for x in wms_words)):
                if(not get_href_url(url, href) in info[3]):
                    info[3].append(get_href_url(url, href)) # potential wms
                    info[0].append(remove_protocol(get_href_url(url, href))) # visited sites
                continue

            # RECURSE (goes into an address if it contains reference to covid or corona)
            if(len(info[0]) < site_limit):
                if(any(x in href_lower for x in ["covid", "corona"])):
                    info = parse_for_covid(get_href_url(url, href), state=state, info=info)

    except UnicodeDecodeError as e:
        print(e)
    return info

def print_parse_for_covid(address, url=None, state=None, site_limit = 50):
    ''' Prints the results of a parse_for_covid(...) call in a clean format'''
    startTime = time.time()
    info = parse_for_covid(address, url, state, site_limit)
    if(state==None):
        state = ""
    results = "\n%s Results:\n\nRelated Sites:\n%a\nPotential Files for Download:\n%a\nPotential Web Mapping Services:\n%a\n" %(state, info[1], info[2], info[3])
    results += "Time elapsed: " + str(time.time() - startTime) + "\n"
    print(results)
    return results

def log(message):
    if(LOGGING):
        print(message)

def parse_all_for_covid(hd_tuples):
    with open("output.txt", "w") as output_file:
        start_time = time.time()
        for hd in hd_tuples:
            output_file.write(print_parse_for_covid(hd[1], state=hd[0], site_limit=50))
        time_message = "Time elapsed: " + str(time.time() - start_time)
        output_file.write(time_message)
        print(time_message)

def main():
    #print_parse_for_covid(HD_PATH + "Oregon Health Authority, Public Health Division.html", "https://www.oregon.gov/oha/ph/pages/index.aspx", state="Oregon", site_limit=50)
    #two_test = get_test_hd_tuples(2)
    parse_all_for_covid(get_hd_tuples())

if __name__ == "__main__":
    main()

# Look into this:
# http://www.healthdata.org/covid/data-downloads