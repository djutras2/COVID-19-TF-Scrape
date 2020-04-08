from bs4 import BeautifulSoup

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","District of Columbia", "Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

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

save_hd_urls()