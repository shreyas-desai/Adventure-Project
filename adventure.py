import argparse
import sys
import json

def look(current_room,data):
    print(f"> {(data[current_room]['name'])}\n")
    print(f"{data[current_room]['desc']}\n")
    if 'items' in data[current_room].keys() and len(data[current_room]['items'])!=0:
        print(f"Items: {', '.join(data[current_room]['items'])}\n")
    print(f"Exits: {' '.join(data[current_room]['exits'].keys())}\n")


def parse_map(map_file):
    data = json.load(map_file)
    current_room = 0
    look(current_room,data)
    current_room_data = data[current_room]
    items = []
    while True:
        try:
            current_room_data = data[current_room]
            verb = input("What would you like to do? ").lower()
            if 'quit' in verb:
                sys.exit("Goodbye!")
            if 'go' in verb.split(' ')[0]:
                try:
                    exit = verb.split(' ')[1]
                    assert exit != ''
                    if exit in current_room_data['exits']:
                        print(f"You go {exit}.\n")
                        current_room = current_room_data['exits'][exit]
                        look(current_room,data)
                    else:
                        print(f"There's no way to go {exit}.")
                except:
                    print("Sorry, you need to 'go' somewhere.")
            
            if 'look' in verb:
                try:
                    look(current_room,data)
                except Exception as e:
                    print(e)

            if 'get' in verb:
                try:
                    item = " ".join(verb.split(' ')[1:]).strip()
                    if 'items' in data[current_room].keys() and len(data[current_room]['items'])!=0 and item in data[current_room]['items']:
                        data[current_room]['items'].remove(item)
                        print(f'You pick up the {item}.')
                        items.append(item)
                    else:
                        print(f"There's no {item} anywhere.")
                except:
                    print("Sorry, you need to 'get' something.")
                        
            
            if 'inventory' in verb:
                try:
                    assert len(items)!=0
                    print("Inventory:")
                    for item in sorted(items):
                        print(f"  {item}")
                except:
                    print("You're not carrying anything.")
        except EOFError:
            print("Use 'quit' to exit.")



def main():
    parser = argparse.ArgumentParser(description = 'Get the map file to start playing!')
    parser.add_argument('map_file',nargs=1, type=argparse.FileType("r"), help="File to read the map from")
    args = parser.parse_args()
    parse_map(args.map_file[0])


if __name__=='__main__':
    main()