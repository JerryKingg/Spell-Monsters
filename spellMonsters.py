import random

player = [1, 1, 1, 1, 20, 20] #(airSkill, fireSkill, waterSkill, earthSkill, maxHealth, health)

spellbook = []
monsters = []
#row spell type's effectiveness against column monster type
#               a    f    w    e    
damageMatrix=[[.50, .75, 2.0, 1.0],# a
              [2.0, .50, 1.0, .75],# f
              [.75, 1.0, .50, 2.0],# w
              [1.0, 2.0, .75, .50]]# e


#return the name associated with a given element number
def getElement(a):
    if (a == 0):
        return "Air"
    if (a == 1):
        return "Fire"
    if (a == 2):
        return "Water"
    if (a == 3):
        return "Earth"
        
        
def makeSpellbook():
    #spellbook = []        #make sure spellbook is empty
    for i in range(4):         #build spellbook
        spellbook.append([])   #make new list
        spellbook[i].append(round(random.random()*3)) #spelltype
        spellbook[i].append(round((random.random()*10)+10)) #spelldamage

def printSpellbook():
    for i, val in enumerate(spellbook):
        print('Spell {}: '.format(i) + getElement(spellbook[i][0]) + " spell")
        print('Damage: {} \n'.format( .5 * spellbook[i][1] * player[spellbook[i][0]] )) #Multiply base damage by the player's elemental skill
    
def makeMonsters():
    #monsters = [] #make sure monster array is empty
    for i in range(4):
        monsters.append([])  #make new list
        monsters[i].append(round(random.random()*3)) #generate type
        monsters[i].append(round((player[0]+player[1]+player[2]+player[3])*(1+random.random()))) #generate health based on total player power
        monsters[i].append(round(player[4]*random.random()*.75)) #generate attack power based on max player health
        
def printMonsters():
    for i, val in enumerate(monsters):
        if(monsters[i][1] > 0):
            print(getElement(monsters[i][0]) + ' monster{}:'.format(i))
            print('HP: {} Attack: {} \n'.format(monsters[i][1], monsters[i][2]))
        
def printPlayer():
        print('Player stats: \n HP: {}/{} \n Air Skill: {} \n Fire Skill: {} \n Water Skill: {} \n Earth Skill: {}'.format(player[4],player[5],player[0],player[1],player[2],player[3])) 
    
def healPlayer():
    player[5] = player[5]+player[0]+player[1]+player[2]+player[3] #heal player by the sum of their skill
    
    if (player[5]>player[4]):
        player[5]=player[4]
        
        
def playerCombat():
    print('Pick a spell:')
    printSpellbook()
    print('Spell Choice: ')
    spell = int(input())
    print('Pick a target:')
    printMonsters()
    print('Target: ')
    target = int(input())
    #damage = player's elemental skill level * base spell damage *  value from rock paper scissors matrix * 1/2 to make it less powerful
    spellDamage = player[spellbook[spell][0]] * spellbook[spell][1] * damageMatrix[spellbook[spell][0]][monsters[target][0]] * .5
    monsters[target][1] = monsters[target][1] - spellDamage
    print('Monster {} took {} damage!'.format(target,spellDamage))
    
    #if the monster dies increase the player's corresponding elemental skill and remove the monster
    if(monsters[target][1] < 0):
        player[monsters[target][0]] = player[monsters[target][0]] + 1
        print('The ' + getElement(monsters[target][0]) + ' monster is killed!')
        print('your ' + getElement(monsters[target][0]) + ' skill is increased by 1!')
        monsters.pop(target)
    
        
    

def playerTurn():
    printPlayer()
    print('What will you do? \n Heal \n Attack \n Decision:')
    decision = input()
    if (decision == 'heal'):
        healPlayer()
    if (decision == 'attack'):
        printMonsters()
        playerCombat()
    

def monsterTurn():
    liveMonsters = 0
    for i, val in enumerate(monsters):
        if(monsters[i][1] > 0):
            damage = (monsters[i][2]/player[monsters[i][0]])#divide monster damage by player elemental skill
            player[5] = player[5]- damage #damage player's health
            print(getElement(monsters[i][0]) + ' monster dealt {} damage to you'.format(damage))
            printPlayer()
            liveMonsters = liveMonsters + 1
            
    if (liveMonsters == 0): #if all monsters are dead regenerate monsters
        print('The final monster lies dead before you, yet you hear strrange noises in the distance..')        
        makeMonsters()
        player[4]=player[4]+4
        healPlayer()
        
    
        
def game():
    makeSpellbook()
    makeMonsters()
    while(player[5]>0):
            playerTurn()
            monsterTurn()
            
    print('You Died')
    

        
        
