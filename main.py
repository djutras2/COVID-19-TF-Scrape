from src import states
from src.StandardLogger import StandardLogger
import os
import sys

test = False
to_test = "Arizona"

logger = StandardLogger("main")

def log(area, function):
    if(test and area != to_test):
        return
    try:
        logger.info("Scraping data from " + area)
        function()
    except Exception as e:
        logger.warn("Unable to scrape data from " + area, e)
        logger.error(e)


def main():
    # TODO: this is terrible. Will come back to make this all neater.
    # logger = StandardLogger("main")

    log("Arizona", states.fetch_az)

    log("North Carolina", states.fetch_nc)

    log("Hamilton, Ohio", states.fetch_hamilton_oh)

    log("Illinois", states.fetch_illinois)

    log("Maryland", states.fetch_maryland)

    log("New York City", states.fetch_nyc)

    log("Oakland, Michigan", states.fetch_oakland_mi)

    log("Pennsylvania", states.fetch_pa)

    log("South Carolina", states.fetch_sc)

    log("St. Louis, Missouri", states.fetch_st_louis_mo)

    log("Florida", states.fetch_florida)
        
    log("Virginia", states.fetch_virginia)

if __name__ == "__main__":
    if(len(sys.argv) > 1) and os.path.exists(sys.argv[1]):
            states.set_path(sys.argv[1])
    else:
        print("Invalid path.")
        states.set_path(".\\output")

    main()
