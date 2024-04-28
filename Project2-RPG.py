import random
"""
CODE DESCRIPTION:
This program is a game where you go around a map collecting items and fighting enemies. You win by
defeating all the enemies and lose when you die. The game is mostly luck as your damage multiples significantly.
As well as the damage you receive.
You can also choose the size of your adventure and get an output text file of your attempt.
"""
"""
The MiniMap class takes in a side length and creates a square 2D list of the same size. It creates a row for
the side length and adds an element for each column. The prinr_map function takes the created map and prints
it out formatted. It checks for what is in the list and outputs without the players movements. Output_map_list adds the map
elements to strings in a list with the players movements This list is then returned.
"""
class MiniMap:
    def __init__(self, size):
        self.length = size
        self.minimap = self.make_map()
    
    def make_map(self):
        minimap = [[' ' for col in range(self.length)] for row in range(self.length)]
        return minimap

    def print_map(self):
        for row in self.minimap:
            for col in row:
                if len(col) == 2:
                    print(f'[{col}]', end='')
                else:
                    if col in ('X', ' '):
                        print(f'[  ]', end='')
                    else:
                        print(f'[{col} ]', end='')
            print()

    def output_map_list(self):
        map_list = []
        for row in self.minimap:
            map_row = ''
            for col in row:
                if len(col) == 2:
                    map_row += f'[{col}]'
                elif col == 'X':
                    map_row += '[XX]'
                else:
                    map_row += f'[{col} ]'
            map_list.append(map_row)
        return map_list
"""
MapIcon class takes in a dictionary and the 2D minimap list. To add an icon it takes a random integer in the
range of the rows and columns. It then checks to see if the space is already taken. If it is then it will pick
different coordinates until its empty and add the character. It gets the icon from the inserted dictionary
keys and takes the first element in its list values. This first element is the icon added to the list.
"""
class MapIcon:
    def __init__(self, icon_dict, minimap):
        self.icon_dict = icon_dict
        self.map = minimap
        self.keys_list = list(icon_dict.keys())

    def add_icon_random(self):
        for icon in self.keys_list:
            while True:
                row = random.randint(0, len(self.map) - 1)
                col = random.randint(0, len(self.map[row]) - 1)
                if self.map[row][col] == ' ':
                    self.icon_dict[icon].append((col, row)) #Adds tuple with coordinates.
                    self.map[row][col] = self.icon_dict[icon][0] #Adds icon to map.
                    break
"""
The player class is a MapIcon that can get randomly placed (spawn) on the map with add_icon_random.
It takes these traits from the MapIcon superclass. It has its own unique details like health, defense, and damage.
It also sets if the player has received any upgrades to their stats. It allows the player to move around
the map, interact with things, change their stats, attack, and receive damage.
"""
class Player(MapIcon):
    def __init__(self, icon_dict, minimap):
        super().__init__(icon_dict, minimap)
        self.health = 100
        self.defense = 0
        self.damage = 1
        self.health_up = False
        self.armor = False
        self.sword = False
    """
    This funtion takes directional inputs 'w', 'a', 's', or 'd' to move up, left, down, or right. The players location is represented
    represented in the list with the third element being a tuple containing location coordinates. These coordinates are received
    and assigned to x and y. Then the temporary x and y values are also made incase the move is invalid. It loops until a valid input is made
    as well.
    """
    def move(self, direction):
        self.direction = direction
        x, y = self.icon_dict['player'][2]
        temp_x, temp_y = x, y #Saves original x and y.
        while True:
            if direction == 'w':
                y -= 1
                break
            elif direction == 'a':
                x -= 1
                break
            elif direction == 's':
                y += 1
                break
            elif direction == 'd':
                x += 1
                break
            else:
                print('Please make a valid input.')
                direction = input().lower().strip() #Receives new direction and formats it.
                
        """
        This checks to see if the player is moving to a taken space or an area out of the 2D list's index.
        If it is a possible move then the player icon is removed and moved to the selected space.
        If something is there it checks to see if an interactable is there and calls the interact function.
        If the space is unable to go to the x and y tuple is set back to the original values.
        """
        if 0 <= x < len(self.map) and 0 <= y < len(self.map):
            if self.map[y][x] in ('X', ' '):
                self.map[temp_y][temp_x] = 'X'
                self.icon_dict['player'][2] = (x, y)
                self.map[y][x] = self.icon_dict['player'][0]
            else:
                self.interact(x, y) #Calls interact function.
        else:
            self.icon_dict['player'][2] = (temp_x, temp_y) #Sets player x and y back to original.
            print("Sorry you can't go here!")
    """
    This takes in x,y coordinates and checks what symbol is in that space. It is set to have an item as none.
    It turns the dictionary for enemies and items into lists containing only the icons. For items, it checks if
    the symbol in the space matches anything in the list. If it does it retrieves the key that is the items name
    and ends the loop. If the found item name is in the item dictionary, it then adds it the the players dictionary value list
    with the inventory as the second element.
    """
    def interact(self, x, y):
        symbol = self.map[y][x]
        item_name = None
        item_list = [item[0] for item in list(item_dict.values())] #Creates item value list with their icons.
        enemy_list = [enemy[0] for enemy in list(enemies_dict.values())] #Creates enemy value list with their icons.
        if symbol in item_list:
            for key, value in item_dict.items(): #Check if symbol matches a dictionary value.
                if value[0][0] == symbol:
                    item_name = key
                    break
            if item_name in item_dict:
                print(f'You found {item_name}!\n{item_dict[item_name][1]}') #Prints out description from list.
                self.icon_dict['player'][1].append(item_name) #Adds item to inventory.
                self.map[y][x] = ' ' #Removes item from map.
                self.change_stats() #Updates stats.
        """
        For enemies, it checks to see if the symbol is in the list of enemy symbols.
        It then retrieves the key value for the enemy if it is found. If there is an enemy, it creates an
        enemy class and then a battle class. The player class and then enemy class are then put into the initiate battle
        function to start a battle. The loop is then ended. It works pretty much the same as the item interaction.
        """
        if symbol in enemy_list:
            for key, value in enemies_dict.items(): #Checks if symbol matches a dictionary value.
                if value[0] == symbol:
                    enemy_name = key
                    enemy = Enemy(enemies_dict, enemy_name) #Creates enemy class with found enemy name.
                    battle = Battle() #Creates battle class.
                    battle.initiate_battle(self, enemy) #Inputs player class and enemy class into initiate battle.
                    break
    """
    This funtion checks the players inventory list for any of the items in their inventory. If the item
    is present then the players stats get updated. It sets that they have the item to True.
    """
    def change_stats(self):
        if 'health' in player['player'][1] and not self.health_up:
            self.health += 100 
            print('Your health increased!\nYour max health is now 100.')
            self.health_up = True
        if 'armor' in player['player'][1] and not self.armor:
            self.defense = 10
            print(f'Your defense increased!\nDamage is now reduced by {self.defense:.0f}.')
            player['player'][0] = 'P'
            self.armor = True
            if self.sword == True:
                player['player'][0] += '/'
        if 'a sword' in player['player'][1] and not self.sword:
            self.damage = 15
            print(f'Your damage increased!\nYou now do {self.damage} damage.')
            player['player'][0] += '/'
            self.sword = True
# This receives a number and multiplies the damage by the number and returns it.
    def attack(self, result):
        damage = self.damage * result
        return damage
# This takes the damage received and subtracts the defense value from it. The players health is then lowered by the damage received.
    def take_damage(self, damage):
        self.health -= (damage - self.defense)
"""
The enemy class takes a dictionary and takes the health, defense, and damage from its value list.
These are then set to the enemies health, defense, and damage stats. It also sets the key to the name.
"""
class Enemy:
    def __init__(self, dict, name):
        health, defense, damage = dict[name][1]
        self.health = health
        self.defense = defense
        self.damage = damage
        self.name = name
# This takes in an integer and multiplies its damage by the amount and returns the damage.
    def attack(self, result):
        damage = self.damage * result
        return damage
# This subtracts the damage received by their defense and subtracts this from the health.
    def take_damage(self, damage):
        self.health -= (damage - self.defense)
"""
The battle class takes in a player and enemy class instance. The won_battle variable is then made global. This battle
will continue until the player or enemies health goes below 0. The roll dice function is called for the enemy and player and
this value is put into their attack functions. Then the damage returned is put into the take_damage function for each. After each attack
the player and bandits health are outputted.

"""
class Battle:
    def initiate_battle(self, player, enemy):
        self.player = player
        self.enemy = enemy
        global won_battle #Gets global won_battle
        print(f"Uh oh it's {self.enemy.name}! Get ready!")
        """
        The player goes first and their roll result is input into roll_print. The result is also input into the player's damage
        function. This damage is input into the enemies take_damage function.
        """
        while self.player.health > 0 and self.enemy.health > 0:
            result = self.roll_dice()
            self.roll_print(result)
            p_damage = self.player.attack(result)
            self.enemy.take_damage(p_damage)
            if self.enemy.health < 0: #Prevents negative health output.
                print("Bandit Health: 0") 
            else:
                print(f"Bandit Health: {self.enemy.health}")
            """
            If the bandit is beaten then the coordinates are retrieved from a tuple in the dictionary.
            This spot on the map is then set to ' '. The enemy is then deleted
            from the enemy dictionary and won battle is set to true.
            """
            if self.enemy.health <= 0:
                print(f"What!!! You actually won? You beat {self.enemy.name}!")
                x, y = enemies_dict[self.enemy.name][2]
                self.player.map[y][x] = ' ' #Removes enemy.
                del enemies_dict[self.enemy.name] #Removes enemy from dictionary.
                won_battle = True
                break
            """
            The enemy rolls and their damage is calculated and damages the player.
            The player takes damage until their health goes below zero and ends the battle.
            """
            result = self.roll_dice()
            e_damage = self.enemy.attack(result)
            self.player.take_damage(e_damage)
            if self.player.health < 0: #Prevents negative health output.
                print("Your Health: 0")
            else:
                print(f"Your Health: {self.player.health}")
            if self.player.health <= 0: #Checks if player loses.
                print("Womp womp better luck next time!")
                break

    def roll_dice(self): #Uses random modules randint to get an integer between 1 and 6 and return the result.
        result = random.randint(1, 6)
        return result
    """
    This is a dictionary with keys matching inters 1-6. The values contain images of the dice and a message for each roll type.
    A set containing messages is another element in the list of values.
    """
    def roll_print(self, result):
        dice_dict = {
            "1": ["""
            +---------------+
            |               |
            |               |
            |      +-+      |
            |      +-+      |
            |               |
            |               |
            +---------------+
            You Rolled a 1...
            """, {"""                    ⡴⠒⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠉⠳⡆⠀
                    ⣇⠰⠉⢙⡄⠀⠀⣴⠖⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠁⠙⡆
                    ⠘⡇⢠⠞⠉⠙⣾⠃⢀⡼⠀⠀⠀⠀⠀⠀⠀⢀⣼⡀⠄⢷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠰⠒⠲⡄⠀⣏⣆⣀⡍
                    ⠀⢠⡏⠀⡤⠒⠃⠀⡜⠀⠀⠀⠀⠀⢀⣴⠾⠛⡁⠀⠀⢀⣈⡉⠙⠳⣤⡀⠀⠀⠀⠘⣆⠀⣇⡼⢋⠀⠀⢱
                    ⠀⠘⣇⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⡴⢋⡣⠊⡩⠋⠀⠀⠀⠣⡉⠲⣄⠀⠙⢆⠀⠀⠀⣸⠀⢉⠀⢀⠿⠀⢸
                    ⠀⠀⠸⡄⠀⠈⢳⣄⡇⠀⠀⢀⡞⠀⠈⠀⢀⣴⣾⣿⣿⣿⣿⣦⡀⠀⠀⠀⠈⢧⠀⠀⢳⣰⠁⠀⠀⠀⣠⠃
                    ⠀⠀⠀⠘⢄⣀⣸⠃⠀⠀⠀⡸⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠈⣇⠀⠀⠙⢄⣀⠤⠚⠁⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⢘⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⢰⣿⣿⣿⡿⠛⠁⠀⠉⠛⢿⣿⣿⣿⣧⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⣸⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⡀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠹⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⡿⠁⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣤⣞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢢⣀⣠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⢤⣀⣀⠀⢀⣀⣀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    - Art from ascii art site"""}],

            "2": ["""
            +---------------+
            |               |
            |               |
            |   +-+   +-+   |
            |   +-+   +-+   |
            |               |
            |               |
            +---------------+
            You Rolled a 2..
            """, {"That's \"two\" bad!", "Better luck nex time!", "Two..."}],

            "3": ["""
            +---------------+
            |               |
            |               |
            | +-+  +-+  +-+ |
            | +-+  +-+  +-+ |
            |               |
            |               |
            +---------------+
            You Rolled A 3.
            """, {"I'd say it's pretty average.", "Third time's the charm!", "Three?"}],

            "4": ["""
            +---------------+
            |  +-+     +-+  |
            |  +-+     +-+  |
            |               |
            |               |
            |  +-+     +-+  |
            |  +-+     +-+  |
            +---------------+                                      
            You Rolled A 4!
            """, {"$4 for $4!", "Keep moving four-ward!", ":0"}],

            "5": ["""
            +---------------+
            |  +-+     +-+  |
            |  +-+     +-+  |
            |      +-+      |
            |      +-+      |
            |  +-+     +-+  |
            |  +-+     +-+  |
            +---------------+                                      
            You Rolled A 5!!
            """, {"I wish you rolled a one!", "Take five!", "Cause if it were freddy five bear"}],

            "6": ["""
            +---------------+
            | +-+  +-+  +-+ |
            | +-+  +-+  +-+ |
            |               |
            |               |
            | +-+  +-+  +-+ |
            | +-+  +-+  +-+ |
            +---------------+
            You Rolled A 6!!!
            """, {"Woah!", "I wish you rolled a 1!\nCongrats I guess.", "Oh yeah!!"}]
        }

        print(dice_dict[str(result)][0]) #Prints out the dice image for the roll result received.
        message = list(dice_dict[str(result)][1]) #Creates a list containing messages from the message set.
        print(random.choice(message)) #Prints a random message from the list.
#Creates player dictionary with icon and inventory list.
player = {
    'player' : ['p', []]
}
#Creates item dictionary with icon and description.
item_dict = {
    'a sword' : ['s', 'This sword was once used (wow).'],
    'health' : ['h', 'Your total health has increased.'],
    'armor' : ['a', 'Despite how it looks this armor offers decent protection.']
}
#Creates enemy dictionary and stat values.
enemies_dict = {
    'enemy1' : ['E1', [100, 10, 10]],
    'enemy2' : ['E2', [100, 10, 10]],
    'enemy3' : ['E3', [100, 10, 10]]
}
"""
This is the main game where you pick map size and then move around the map until you win or lose.
Your movements made during the game are then output to a file.
"""
def main():
    """
    Welcomes player and prompts them to pick a size of map. It loops until a valid size is chosen.
    This size is then used to create a MiniMap class of a big, bigger, or biggest size.
    """
    global won_battle #Gets global won_battle
    won_battle = False
    moves = 0 #Sets moves
    enemies_left = 3 #Sets enemies left.
    tries = 0 #Creates tries
    print('Welcome to the game!!!\nPlease choose the size of your adventure. (big, bigger, biggest)')
    while True:
        game_size = input().lower().strip()
        if game_size not in ('big', 'bigger', 'biggest'):
            if tries == 10: #Ends game is the player is messing around
                print("You don't even want to play this game.")
                print("ヽ( `д´*)ノ" * 5)
                exit()
            elif tries > 2: #Checks tries to give different input request messages.
                print(f"STOP!! Youve done this {tries} times!\nPLEASE make a valid input!!")
                tries += 1
            else:
                print("I'm sorry we don't have that size./Please try again.")
                tries += 1
            continue #Continues loop
        else:
            break #Breaks loop

    if game_size == 'big': #For setting the size of the game.
        map_ = MiniMap(6) #Creates the map for the game.
    elif game_size == 'bigger':
        map_ = MiniMap(10)
    elif game_size == 'biggest':
        map_ = MiniMap(17)

    print(f'There are 3 bandits you must stop.\n Please you have to!!!')
    """
    This adds all the items and enemies from their dictionaries to the map.
    The player is then created and added to the map as well.
    """

    item = MapIcon(item_dict, map_.minimap) #Creates items icons.
    enemy = MapIcon(enemies_dict, map_.minimap) #Creates enemies icons.
    item.add_icon_random() #Adds items randomly to map.
    enemy.add_icon_random() #Adds enemies randomly to map.
    p = Player(player, map_.minimap) #Creates player class.
    p.add_icon_random() #Adds player to random spot on map.

    while True:
        map_.print_map() #Prints map.
        d = input("Enter direction (w/a/s/d): ")
        p.move(d) #Moves player.
        moves += 1
        # This checks and counts how many enemies are left. When there are no enemies left the game loop is broken.
        if won_battle:
            enemies_left = len(list(enemies_dict)) #Counts how many enemies are in enemies dictionary.
            won_battle = False
            if enemies_left == 2:
                print('Thats 1 down')
            elif enemies_left == 1:
                print('Just one more!')
            elif enemies_left == 0:
                print('Thank you so much for getting rid of the bandits!')
                break
        if p.health <= 0: #If players health is below 0 the game loop is broken.
            break
    """
    This creates Game_Certificate.txt file and write to it. It writes a message and the tiles the player went to.
    It also adds how many moves they made during the game.
    """
    output_file = "Game_Certificate.txt" #Sets name of output_file.
    with open(output_file, 'w') as file: #Creates Game_Certificate.txt file.
        if enemies_left == 0: #If player wins writes win line.
            file.write("☆ ～('▽^人)\nYou did it!\nCertificate of Completion!\n")
        else: #If player loses writes loss line.
            file.write('╮(︶▽︶)╭\nAtleast you tried.\nCertificate of Incompletion!\n')
        output_map = map_.output_map_list() #Creates list of map strings.
        for row in output_map: #Writes each map string row to file.
            file.write(f'{row}\n')
        if moves == 1:#Checks how many moves made and writes proper message.
            file.write('The "XX" is your journey.\n You made 1 move.')
        else:
            file.write(f'The "XX" is your journey.\n You made {moves} moves.')

if __name__ == "__main__": #Runs main
    main()