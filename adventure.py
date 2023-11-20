import argparse
import sys
import json

def look(current_room,data):
    print(f"> {(data[current_room]['name'])}")
    print()
    print(data[current_room]['desc'])
    print()
    if 'items' in data[current_room].keys() and len(data[current_room]['items'])!=0:
        print(f"Items:",*data[current_room]['items'])
        print()
    print(f"Exits:",*data[current_room]['exits'].keys())
    print()
    

def parse_map(map_file):
    data = json.load(map_file)
    current_room = 0
    look(current_room,data)
    current_room_data = data[current_room]
    while True:
        current_room_data = data[current_room]
        verb = input("What would you like to do? ")
        if 'go' in verb.lower().split(' ')[0]:
            try:
                if verb.lower().split(' ')[1] in current_room_data['exits']:
                    print(f"You go {verb.lower().split(' ')[1].lower()}")
                    current_room = current_room_data['exits'][verb.lower().split(' ')[1]]
                    print(current_room)
                    look(current_room,data)
                else:
                    print(f"There's no way to go {verb.lower().split(' ')[1].lower()}")
            except:
                print("Sorry you need to go somewhere")
        
        if 'look' in verb.lower():
            try:
                look(current_room,data)
            except Exception as e:
                print(e)



def main():
    parser = argparse.ArgumentParser(description = 'Get the map file to start playing!')
    parser.add_argument('map_file',nargs='?', type=argparse.FileType("r"), help="File to read the map from")
    args = parser.parse_args()
    if args.map_file:
        parse_map(args.map_file)
    else:
        print("Give a MAP!!")
        sys.exit()

if __name__=='__main__':
    main()