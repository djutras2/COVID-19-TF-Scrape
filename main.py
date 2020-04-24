from src import states
import os
import sys

def main():
    #TODO: this is terrible. Will come back to make this all neater.
    states.fetch_florida()
    states.fetch_hamilton_oh()
    states.fetch_illinois()
    states.fetch_maryland()
    states.fetch_nyc()
    states.fetch_oakland_mi()
    states.fetch_phil_pa()
    states.fetch_sc()
    states.fetch_st_louis_mo()

if __name__ == "__main__":
    if(len(sys.argv) > 1) and os.path.exists(sys.argv[1]):
            states.set_path(sys.argv[1])
    else:
        print("Invalid path.")
        states.set_path(".\\output")

    main()