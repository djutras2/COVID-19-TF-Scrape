from bs4 import BeautifulSoup
import random
from words import states

def extract_hds():
    '''Extracts all health department links from the (pre-extracted) CDC website'''
    soup = BeautifulSoup(open("./State and Territorial Health Department Websites.html"), "html.parser")
    urls = []
    names = []
    for a in soup.select("a"):
        urls.append(a.get("href"))
        names.append(a.contents[0])
    return names, urls

def get_state(name):
    words = name.split()
    for i in range(4):
        for i in range(1, i+1):
            word = " ".join(words[:i])
            if(word in states):
                return word
    return words[0]

def save_hd_urls():
    hds = extract_hds()
    with open("state_hd_list.txt", "w") as hd_list:
        for name, url in zip(hds[0], hds[1]):
            if not name == None and not url == None:
                hd_list.write(get_state(name) + "\t" + url + "\n")

def get_hd_tuples():
    '''Returns a list of tuples of the form (state, url)'''
    states = []
    with open("state_hd_list.txt", "r") as hd_list:
        for hd_entry in hd_list:
            hd = hd_entry.split("\t")
            states.append((hd[0], hd[1].strip()))
    return states

def get_test_hd_tuples(amount):
    '''Returns random subset of a list of tuples of the form (state, url)'''
    states = get_hd_tuples()
    subset = []
    for _ in range(amount):
        choice = random.choice(states)
        subset.append(choice)
        states.remove(choice)
    return subset

# def extract_hds():
#     '''Extracts all health department info from the CDC website'''
#     soup = BeautifulSoup(open("./State and Territorial Health Department Websites.html"), "html.parser")
#     urls = []
#     names = []
#     for a in soup.select("a"):
#         urls.append(a.get("href"))
#         names.append(a.contents[0])
#     return names, urls

# def save_hd_urls():
#     hds = extract_hds()
#     with open("hd_list", "w") as hd_list:
#         for name, url in zip(hds[0], hds[1]):
#             if not name == None and not url == None:
#                 hd_list.write(name + "\t" + url)