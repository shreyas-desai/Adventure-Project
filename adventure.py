import argparse
import json

class Game:
    def __init__(self, world_map):
        self.world_map = world_map
        self.current_room = 0
        self.items = []

    def look(self):
        current_room_data = self.world_map[self.current_room]
        print(">", current_room_data['name'],"\n")
        # print()
        print(current_room_data['desc'],"\n")
        # print()
        if 'items' in current_room_data and len(current_room_data['items']) != 0:
            print(f"Items: {', '.join(current_room_data['items'])}\n")
            # print()
        print(f"Exits: {' '.join(current_room_data['exits'])}\n")
        # print()

    def go(self, exit_name):
        current_room_data = self.world_map[self.current_room]
        if exit_name in current_room_data['exits']:
            print(f"You go {exit_name}.\n")
            # print()
            self.current_room = current_room_data['exits'][exit_name]
            self.look()
        elif exit_name=='':
            print("Sorry, you need to 'go' somewhere.")
        else:
            print(f"There's no way to go {exit_name}.")

    def get(self, item):
        current_room_data = self.world_map[self.current_room]
        if 'items' in current_room_data and len(current_room_data['items']) != 0 and item in current_room_data['items']:
            current_room_data['items'].remove(item)
            print(f'You pick up the {item}.')
            self.items.append(item)
        elif item=='':
            print("Sorry, you need to 'get' something.")
        else:
            print(f"There's no {item} anywhere.")

    def inventory(self):
        if len(self.items) == 0:
            print("You're not carrying anything.")
            return
        print("Inventory:")
        for item in sorted(self.items):
            print(f"  {item}")

def parse_map(map_file):
    data = map_file
    game = Game(data)
    game.look()

    while True:
        try:
            verb = input("What would you like to do? ").lower().strip()

            if 'quit' in verb:
                print("Goodbye!")
                quit()
            elif 'go' in verb.split()[0]:
                game.go(' '.join(verb.split()[1:]))
            elif 'look' in verb:
                game.look()
            elif 'get' in verb:
                game.get(' '.join(verb.split()[1:]))
            elif 'inventory' in verb:
                game.inventory()
        except EOFError:
            print("Use 'quit' to exit.")

def main():
    parser = argparse.ArgumentParser(description='Get the map file to start playing!')
    parser.add_argument('map_file', help="File to read the map from")
    args = parser.parse_args()

    with open(args.map_file) as f:
        world_map = json.load(f)
    parse_map(world_map)

if __name__ == '__main__':
    main()
