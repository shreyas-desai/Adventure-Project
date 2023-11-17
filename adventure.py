import argparse
import sys
import json

def parse_map(map_file):
    data = json.load(map_file)
    print(f"> {(data[0]['name'])}")
    print()
    print(data[0]['desc'])
    print()
    print(f"Exits:",*data[0]['exits'].keys())
    print()
    while True:
        print("What would you like to do?")
        break

def main():
    parser = argparse.ArgumentParser(description = 'Get the map file to start playing!')
    parser.add_argument('map_file',nargs='?', type=argparse.FileType("r"), default=sys.stdin, help="File to read the map from")
    args = parser.parse_args()
    parse_map(args.map_file)

if __name__=='__main__':
    main()