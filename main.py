from src import states
from src.StandardLogger import StandardLogger
import os
import sys


def main():
    logger = StandardLogger("main")
    # TODO: this is terrible. Will come back to make this all neater.

    try:
        logger.info("Scraping data from Hamilton, Ohio")
        states.fetch_hamilton_oh()
    except Exception as e:
        logger.warn("Unable to scrape data from Hamilton, Ohio", e)

    try:
        logger.info("Scraping data from Illinois")
        states.fetch_illinois()
    except Exception as e:
        logger.warn("Unable to scrape data from Illinois", e)

    try:
        logger.info("Scraping data from Maryland")
        states.fetch_maryland()
    except Exception as e:
        logger.warn("Unable to scrape data from Maryland", e)

    try:
        logger.info("Scraping data from New York City")
        states.fetch_nyc()
    except Exception as e:
        logger.warn("Unable to scrape data from New York City", e)

    try:
        logger.info("Scraping data from Oakland, Michigan")
        states.fetch_oakland_mi()
    except Exception as e:
        logger.warn("Unable to scrape data from Oakland, Michigan", e)

    try:
        logger.info("Scraping data from Philadelphia, Pennsylvania")
        states.fetch_phil_pa()
    except Exception as e:
        logger.warn("Unable to scrape data from Philadelphia, Pennsylvania", e)

    try:
        logger.info("Scraping data from South Carolina")
        states.fetch_sc()
    except Exception as e:
        logger.warn("Unable to scrape data from South Carolina", e)

    try:
        logger.info("Scraping data from St. Louis, Missouri")
        states.fetch_st_louis_mo()
    except Exception as e:
        logger.warn("Unable to scrape data from St. Louis, Missouri", e)

    try:
        logger.info("Scraping data from Florida")
        states.fetch_florida()
    except Exception as e:
        logger.warn("Unable to scrape data from Florida", e)


if __name__ == "__main__":
    if(len(sys.argv) > 1) and os.path.exists(sys.argv[1]):
            states.set_path(sys.argv[1])
    else:
        print("Invalid path.")
        states.set_path(".\\output")

    main()
