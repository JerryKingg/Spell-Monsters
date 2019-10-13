        self.maxhp=20
        
    def heal(self): #heals by half of player's total elemental skill
        self.hp = self.hp + .5 *(self.airskill + self.fireskill + self.waterskill + self.earthskill)
        if (self.hp > self.maxhp):
            self.hp = self.maxhp
            
    def printPlayer(self):
        print('/nPlayer stats: \n Health: {}/{} \n Air Skill: {} \n Fire Skill: {} \n Water Skill: {} \n Earth Skill: {} \n'.format(self.hp, self.maxhp, self.airskill, self.fireskill, self.waterskill, self.earthskill))
    
class Spell:
    def __init__(self):
        self.element = random.randrange(4)
        self.damage = 9+random.randrange(6)
        
    def __init__(self, el, power):
        self.element = el
        self.damage = power
    
    
class Monster:
    def __init__(self):
        self.element = random.randrange(4)
        self.hp = 15
        self.attack = random.randrange(4)
    


def getElement(a):
    if (a == 0):
        return "Air"
    if (a == 1):
        return "Fire"
    if (a == 2):
        return "Water"
    if (a == 3):
        return "Earth"
        

def game(): #sets up a game and runs it till the player dies
    player = Player()
    spellbook = []
    monsterGang = []
    # row element's attack effectiveness against col element
    #              a    f    w    e
    rocPapSci=  ((0.5, .75, 1.0, 2.0), #air row
                 (1.0, 0.5, 2.0, .75), #fire row
                 (.75, 2.0, 0.5, 1.0), #water row
                 (2.0, 1.0, .75, 0.5)) #earth row
    
    def printMonsters():#prints out each monster in the gang 
        for i, val in enumerate(monsterGang):
            print(getElement(monsterGang[i].element)+ ' monster {}:'.format(i))
            print('Health: {}'.format(monsterGang[i].hp))
            print('Attack: {} \n'.format(monsterGang[i].attack))
                        
    def printSpellbook():#prints out each spell in the list with it's attributes
        for i, val in enumerate(spellbook):
            spelldamage = .7
            if(spellbook[i].element==0):
                spelldamage = (spelldamage + (player.airskill*.3))*spellbook[i].damage
            if(spellbook[i].element==1):
                spelldamage = (spelldamage + (player.fireskill*.3))*spellbook[i].damage
            if(spellbook[i].element==2):
                spelldamage = (spelldamage + (player.waterskill*.3))*spellbook[i].damage
            if(spellbook[i].element==3):
                spelldamage = (spelldamage + (player.earthskill*.3))*spellbook[i].damage
            print(getElement(spellbook[i].element) + 'spell {}'.format(i))
            print('Damage: {} \n'.format(round(spelldamage,1)))
        
    #fill spellbook with spells
    for i in range(8):
        spellbook.append(Spell(i%4,(7+random.randrange(6))))
        
    while (player.hp > 0):#game loop
        
        #calaculate player power once per loop to efficeintly generate monsters
        playerPower = player.airskill + player.fireskill + player.waterskill + player.earthskill
        
        if(monsterGang == []): #if there are no monsters make some
            for i in range(3):
                monsterGang.append(Monster()) #create a monster
                monsterGang[i].hp = monsterGang[i].hp * playerPower * .22 #scale monster hp by player power
                monsterGang[i].attack = (monsterGang[i].attack + (.1 * player.maxhp)) #scale monster attack strengh by a mixture of player health and player defense
        
        player.printPlayer()
        
        #player's turn
        print('you are confronted by {} monsters \n'.format(len(monsterGang)))
        printMonsters()
        print('What will you do? \n Attack: 1 \n Heal: 2' )
        selection = input('Response: ')
        
        if(int(selection) == 2): #heal the player
            player.heal()
            
        else:  #begin combat
            print('\nPick a spell: \n')
            printSpellbook()  
            spell = int(input('Spell:'))
            print('\nSelect target:')
            printMonsters()
            target = int(input('Target:'))
            
            spelldamage=.7 #base damage
                           #damage is scaled by player's elemental skill
            if(spellbook[spell].element==0):
                spelldamage = spelldamage + (player.airskill*.3)
            if(spellbook[spell].element==1):
                spelldamage = spelldamage + (player.fireskill*.3)
            if(spellbook[spell].element==2):
                spelldamage = spelldamage + (player.waterskill*.3)
            if(spellbook[spell].element==3):
                spelldamage = spelldamage + (player.earthskill*.3)
            
            #use the rock paper scissors matrix to modify elemental spell damage besed on monster's element
            spelldamage = round(spelldamage*(spellbook[spell].damage * rocPapSci[spellbook[spell].element][monsterGang[target].element]),1)
            
            monsterGang[target].hp = round(monsterGang[target].hp - spelldamage,1)
            print('\n' + getElement(monsterGang[target].element) + ' monster took {} damage!'.format(spelldamage))
            
            if(monsterGang[target].hp <= 0): #if the monster is killed
                
                #level up the player
                if(monsterGang[target].element==0):
                    player.airskill = player.airskill +1
                if(monsterGang[target].element==1):
                    player.fireskill = player.fireskill +1
                if(monsterGang[target].element==2):
                    player.waterskill = player.waterskill +1
                if(monsterGang[target].element==3):
                    player.earthskill = player.earthskill +1
                    
                print(getElement(monsterGang[target].element) + 'monster was killed! \nYour ' + getElement(monsterGang[target].element) + ' skill is increased by 1!\n')
                monsterGang.pop(target)#destroy the targeted monster

        
        
        #monsters' turn
        if(monsterGang == []): #check if all monsters are dead
            player.maxhp = player.maxhp + 3 #level up player health
            print('The final monster lies dead before you, yet you hear something in the distance..')
            player.hp = player.maxhp #heal player to max
            
        else: #all remaining monsters attack
        
            for i, monster in enumerate(monsterGang):
                player.hp = round(player.hp - monster.attack, 1)
                print('\n'+getElement(monster.element) + ' monster dealt {} damage to you! \n'.format(monster.attack))
                print('Health: {}/{} \n'.format(player.hp,player.maxhp))
            
    print('You died!')
    print('Score: {}'.format(player.airskill + player.fireskill + player.waterskill + player.earthskill))
