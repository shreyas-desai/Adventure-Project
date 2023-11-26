import argparse
import json

class Game:
    def __init__(self, world_map):
        self.world_map = world_map
        self.current_room = 0
        self.items = []

    def look(self):
        current_room_data = self.world_map[self.current_room]
        print(">", current_room_data['name'])
        print()
        print(current_room_data['desc'])
        print()
        if 'items' in current_room_data and len(current_room_data['items']) != 0:
            print(f"Items: {', '.join(current_room_data['items'])}")
            print()
        print(f"Exits: {' '.join(current_room_data['exits'])}")
        print()

    def go(self, exit_name):
        current_room_data = self.world_map[self.current_room]
        if exit_name in current_room_data['exits']:
            print(f"You go {exit_name}.")
            print()
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

    # Extension 1 - "drop {item}"
    def drop(self,item):
        current_room_data = self.world_map[self.current_room]
        if item=='':
            print("Sorry, you need to 'drop' something.")
        elif item not in self.items:
            print(f"You are not carrying {item}.")
        else:
            self.items.remove(item)
            current_room_data['items'].append(item)
            print(f"You dropped {item}.")
    
    #Extension 2 - "deny entry if door locked"
    def check_door_locked(self,door):
        current_room_data = self.world_map[self.current_room]
        required = []
        if 'requirements' in current_room_data:
            if door in current_room_data['exits']:
                next_room_data = self.world_map[current_room_data['exits'][door]]
            else:
                print(f"There's no way to go {door}.")
                return False,required
            current_requirements = next_room_data['requirements']
        else:
            return False,required

        
        for req in current_requirements:
            if req not in self.items:
                required.append(req)
        return len(required)>0, required



    def inventory(self):
        if len(self.items) == 0:
            print("You're not carrying anything.")
            return
        print("Inventory:")
        for item in sorted(self.items):
            print(f"  {item}")

def parse_map(map_file):
    data = json.load(map_file)
    game = Game(data)
    game.look()

    while True:
        try:
            verb = input("What would you like to do? ").lower().strip()

            if 'quit' in verb:
                print("Goodbye!")
                quit()
            elif 'go' in verb.split()[0]:
                door = ' '.join(verb.split()[1:])
                is_locked,items = game.check_door_locked(door)
                if not is_locked:
                    game.go(door)
                else:
                    print(f"You need {', '.join(items)} to pass through this door.")
            elif 'look' in verb:
                game.look()
            elif 'get' in verb:
                game.get(' '.join(verb.split()[1:]))
            elif 'drop' in verb:
                game.drop(' '.join(verb.split()[1:]))
            elif 'inventory' in verb:
                game.inventory()
        except EOFError:
            print("Use 'quit' to exit.")

def main():
    parser = argparse.ArgumentParser(description='Get the map file to start playing!')
    parser.add_argument('map_file',nargs=1,type=argparse.FileType('r'), help="File to read the map from")
    args = parser.parse_args()

    parse_map(args.map_file[0])

if __name__ == '__main__':
    main()
