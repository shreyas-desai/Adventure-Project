import argparse
import json

class Game:
    def __init__(self, world_map):
        self.world_map = world_map
        self.current_room = 0
        self.items = []
        self.__verbs__ = ['drop', 'get', 'go', 'help', 'inventory', 'look', 'quit']
        self.__directions__ = ['east', 'west', 'north', 'south', 'northeast', 'northwest', 'southeast', 'southwest']
    
    def look(self):
        """look 
            -- Look around the current room."""
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
        """go ... 
            -- Go in a particular direction. [east, west, south, north, northeast, northwest, southeast, southwest]"""
        current_room_data = self.world_map[self.current_room]
        if exit_name in current_room_data['exits']:
            print(f"You go {exit_name}.")
            print()
            self.current_room = current_room_data['exits'][exit_name]
            self.look()
        elif exit_name == '':
            print("Sorry, you need to 'go' somewhere.")
            return
        else:
            print(f"There's no way to go {exit_name}.")

    def get(self, item):
        """get ... 
            -- Get a specified item."""
        current_room_data = self.world_map[self.current_room]
        if 'items' in current_room_data and len(current_room_data['items']) != 0 and item in current_room_data['items']:
            current_room_data['items'].remove(item)
            print(f'You pick up the {item}.')
            self.items.append(item)
        elif item == '':
            print("Sorry, you need to 'get' something.")
        else:
            print(f"There's no {item} anywhere.")

    def drop(self, item):
        """drop 
            -- Drop items from the inventory in the current room"""
        current_room_data = self.world_map[self.current_room]
        if item == '':
            print("Sorry, you need to 'drop' something.")
        elif item not in self.items:
            print(f"You are not carrying {item}.")
        else:
            self.items.remove(item)
            current_room_data['items'].append(item)
            print(f"You dropped {item}.")

    def __check_door_locked__(self, door):
        """__check_door_locked__ 
            -- check if the door is locked. If required items present in inventory, it is unlocked."""
        current_room_data = self.world_map[self.current_room]
        required = []
        if 'requirements' in current_room_data:
            if door in current_room_data['exits']:
                next_room_data = self.world_map[current_room_data['exits'][door]]
                current_requirements = next_room_data['requirements']
            else:
                return False, required
        else:
            return False, required

        for req in current_requirements:
            if req not in self.items:
                required.append(req)
        return len(required) > 0, required

    def __check_villain__(self, door):
        current_room_data = self.world_map[self.current_room]
        if door in current_room_data['exits']:        
            if "villian" in self.world_map[current_room_data['exits'][door]]:             
                if self.world_map[current_room_data['exits'][door]]['villian'] == "True":

                    return True
        else:
            return False

    def help(self):
        """help
            -- How to play?"""
        function_names = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        for function in function_names:
            func = getattr(self, function)
            if func and callable(func):
                docstring = func.__doc__
                if docstring:
                    print(docstring)

    def inventory(self):
        """inventory 
            -- Show the inventory."""
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
            if verb == '':
                print('You need to enter something!')
                continue
            
            if verb.split()[0] not in game.__verbs__ and verb.split()[0] not in game.__directions__:
                print("No such command!")
                continue

            if 'quit' in verb:
                print("Goodbye!")
                quit()
            elif 'go' in verb.split()[0] or verb.split()[0] in game.__directions__:
                if verb.split()[0] in game.__directions__:
                    door = verb.split()[0]
                else:
                    door = ' '.join(verb.split()[1:])
                if game.__check_villain__(door):
                    decision = input(f"Danger!\nDo you wish to continue?(Y/n)")
                    if 'y' in decision.lower():
                        is_locked, items = game.__check_door_locked__(door)
                        if not is_locked:
                            game.go(door)
                            print(f"You killed the Night King.\nThe wall stands..")
                            quit()
                        else:
                            print(f"The Night King killed you..\nYou died!")
                            quit()
                    else:
                        continue
                else:
                    is_locked, items = game.__check_door_locked__(door)
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
            elif 'help' in verb:
                game.help()
        except EOFError:
            print("Use 'quit' to exit.")

def main():
    parser = argparse.ArgumentParser(description='Get the map file to start playing!')
    parser.add_argument('map_file', nargs=1, type=argparse.FileType('r'), help="File to read the map from")
    args = parser.parse_args()

    parse_map(args.map_file[0])

if __name__ == '__main__':
    main()
