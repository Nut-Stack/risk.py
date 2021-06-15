import pygame
import sys
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Calibri', 20)

WINDOW_HEIGHT = 1700
WINDOW_WIDTH = 900
CIRCLE_SIZE = 45
SMALL_CIRCLE_SIZE = CIRCLE_SIZE - 10
gameDisplay = pygame.display.set_mode((WINDOW_HEIGHT,WINDOW_WIDTH))
drawn = False
crashed = False

ORANGE = (255,127,39)
DEAD_COLOR = (5,5,0)
WHITE = (255, 255, 255)
YELLOW = (35,64,153)
LIGHT_GREEN = (100,200,100)
BROWN = (139,69,19)
RED = (255,50,50)
PINK = (219,112,147)
BLUE = (77,166,255)
Color_line = (100,100,100)
PLAYER1_COLOR = (255,25,25)
PLAYER2_COLOR = (76,230,10)
PLAYER3_COLOR = (51,153,255)
PLAYER4_COLOR = (255,25,255)
PLAYER5_COLOR = (230,230,51)
PLAYER6_COLOR = (255,170,10)
gameDisplay.fill(DEAD_COLOR)

STARTING_TROOPS = 20

'''
TODO

implement what happens when you fail an attack
implement cards
implement turns
implement gain of troops at start of turn
implement troop dropping
implement fortify shit
'''

NA = {
"Alaska":{"x":70,"y":50,"region":"NA","connections":["Northwest Territory","Alberta"]},
"Northwest Territory":{"x":270,"y":50,"region":"NA","connections":["Alaska","Alberta","Ontario","Greenland"]},
"Greenland":{"x":470,"y":50,"region":"NA","connections":["Northwest Territory","Ontario","Quebec","Iceland"]},
"Quebec":{"x":420,"y":150,"region":"NA","connections":["Greenland","Ontario","Eastern US"]},
"Alberta":{"x":140,"y":150,"region":"NA","connections":["Alaska","Northwest Territory","Ontario","Western US"]},
"Ontario":{"x":310,"y":150,"region":"NA","connections":["Northwest Territory","Greenland","Quebec","Eastern US","Western US","Alberta"]},
"Western US":{"x":150,"y":250,"region":"NA","connections":["Alberta","Ontario","Eastern US","Central America"]},
"Eastern US":{"x":400,"y":250,"region":"NA","connections":["Western US","Ontario","Quebec","Central America"]},
"Central America":{"x":275,"y":350,"region":"NA","connections":["Western US","Eastern US","Venezuela"]},

"Venezuela":{"x":275,"y":450,"region":"SA","connections":["Central America","Peru","Brazil"]},
"Brazil":{"x":475,"y":550,"region":"SA","connections":["Venezuela","Peru","Argentina","North AF"]},
"Peru":{"x":275,"y":650,"region":"SA","connections":["Venezuela","Brazil","Argentina"]},
"Argentina":{"x":475,"y":750,"region":"SA","connections":["Peru","Brazil"]},

"Iceland":{"x":650,"y":50,"region":"EU","connections":["Greenland","Scandinavia","Great Britan"]},
"Great Britan":{"x":600,"y":150,"region":"EU","connections":["Iceland","Scandinavia","Northern EU","Western EU"]},
"Scandinavia":{"x":800,"y":50,"region":"EU","connections":["Iceland","Great Britan","Northern EU","Ukraine"]},
"Northern EU":{"x":700,"y":150,"region":"EU","connections":["Great Britan","Scandinavia","Ukraine","Southern EU","Western EU"]},
"Ukraine":{"x":820,"y":170,"region":"EU","connections":["Scandinavia","Ural","Afghanistan","Middle East","Southern EU","Northern EU"]},
"Western EU":{"x":600,"y":300,"region":"EU","connections":["Great Britan","Northern EU","Southern EU","North AF"]},
"Southern EU":{"x":720,"y":300,"region":"EU","connections":["Western EU","Northern EU","Ukraine","Middle East","Egypt","North AF"]},

"North AF":{"x":650,"y":450,"region":"AF","connections":["Western EU","Brazil","Egypt","East AF","Congo","Southern EU"]},
"Egypt":{"x":800,"y":450,"region":"AF","connections":["Southern EU","Middle East","East AF","North AF"]},
"Congo":{"x":670,"y":600,"region":"AF","connections":["North AF","East AF","South AF"]},
"South AF":{"x":700,"y":750,"region":"AF","connections":["Congo","East AF","Madagascar"]},
"Madagascar":{"x":850,"y":750,"region":"AF","connections":["South AF","East AF"]},
"East AF":{"x":800,"y":650,"region":"AF","connections":["Egypt","Madagascar","South AF","Congo","North AF"]},

"Ural":{"x":950,"y":110,"region":"AS","connections":["Ukraine","Siberia","China","Afghanistan"]},
"Siberia":{"x":1050,"y":80,"region":"AS","connections":["Ural","Yakutsk","Irkutsk","Mongolia","China"]},
"Yakutsk":{"x":1200,"y":50,"region":"AS","connections":["Siberia","Kamchatka","Irkutsk"]},
"Kamchatka":{"x":1300,"y":50,"region":"AS","connections":["Yakutsk","Japan","Irkutsk","Mongolia"]},
"Irkutsk":{"x":1185,"y":150,"region":"AS","connections":["Siberia","Yakutsk","Kamchatka","Mongolia"]},
"Mongolia":{"x":1200,"y":250,"region":"AS","connections":["Siberia","Kamchatka","Irkutsk","Japan","China"]},
"Afghanistan":{"x":950,"y":225,"region":"AS","connections":["Ukraine","Ural","China","India","Middle East"]},
"Middle East":{"x":920,"y":340,"region":"AS","connections":["East AF","Egypt","Southern EU","Ukraine","Afghanistan","India"]},
"China":{"x":1200,"y":350,"region":"AS","connections":["India","Afghanistan","Ural","Siberia","Mongolia","Siam"]},
"India":{"x":1037,"y":350,"region":"AS","connections":["Middle East","Afghanistan","China","Siam"]},
"Siam":{"x":1200,"y":485,"region":"AS","connections":["India","China","Indonesia"]},
"Japan":{"x":1400,"y":150,"region":"AS","connections":["Irkutsk","Kamchatka"]},

"Indonesia":{"x":1200,"y":620,"region":"AU","connections":["Siam","New Guinea","West AU"]},
"New Guinea":{"x":1400,"y":620,"region":"AU","connections":["Indonesia","West AU","East AU"]},
"East AU":{"x":1400,"y":820,"region":"AU","connections":["West AU","New Guinea"]},
"West AU":{"x":1200,"y":820,"region":"AU","connections":["East AU","Indonesia","New Guinea"]}
}



player_dict = {}
randomlist = random.sample(range(0,42),42)
for i in range(1,7):#do random shit to generate shit
    player_dict.update({"Player {}".format(i):{"regions":randomlist[0:7]}})
    holder_player_list = []
    for item in randomlist[0:7]:
        randomlist.remove(item)
        while True:
            holder_player_list.append(random.randint(1,7))
            if sum(holder_player_list) == 20 and len(holder_player_list) == 7:
                break
            if sum(holder_player_list) > 20 or len(holder_player_list) > 7:
                holder_player_list.clear()
    player_dict.get("Player {}".format(i)).update({"troops":holder_player_list})

found = False
for num, region in enumerate(NA):#add troops and player ownership
    for player in player_dict:
        for thing in player_dict.get(player).get("regions"):
            if thing == num:
                owner = player
                NA.get(region).update({"owner":owner})
                found = True
        if found == True:
            troops_list = player_dict.get(player).get("troops")
            if type(troops_list) == list:
                first_of_troops = troops_list[0]
                troops_list.remove(first_of_troops)
            else:
                first_of_troops = troops_list
            player_dict.get(player).update({"troops":troops_list})
            NA.get(region).update({"troops":first_of_troops})
            found = False


color_dict = {
"regions":{
"AU":PINK,
"NA":YELLOW,
"SA":ORANGE,
"EU":LIGHT_GREEN,
"AF":BROWN,
"AS":RED},
"players":{
"Player 1":PLAYER1_COLOR,
"Player 2":PLAYER2_COLOR,
"Player 3":PLAYER3_COLOR,
"Player 4":PLAYER4_COLOR,
"Player 5":PLAYER5_COLOR,
"Player 6":PLAYER6_COLOR
}
}

def draw_line(location1, location2):#need to add a log of some sort for each line
    x = NA.get(location1).get("x")
    y = NA.get(location1).get("y")
    x1 = NA.get(location2).get("x")
    y1 = NA.get(location2).get("y")
    pygame.draw.line(gameDisplay, Color_line, (x,y),(x1,y1),5)


player_rects = {}
if drawn == False:
    for region in NA:
        connections = NA.get(region).get("connections")
        for connection in connections:
            draw_line(region,connection)
        pygame.display.flip()
    for region in NA:
        location = (NA.get(region).get("x"),NA.get(region).get("y"))
        troopcount = str(NA.get(region).get("troops"))
        owner = NA.get(region).get("owner")
        x = location[0]
        y = location[1]
        continent_color = color_dict.get("regions").get(NA.get(region).get("region"))
        player_color = color_dict.get("players").get(NA.get(region).get("owner"))
        pygame.draw.circle(gameDisplay,continent_color,location,CIRCLE_SIZE)
        pygame.draw.circle(gameDisplay,player_color,location,SMALL_CIRCLE_SIZE)

        textsurface = myfont.render(region, False, WHITE)#country names
        text_rect = textsurface.get_rect(center=location)
        gameDisplay.blit(textsurface, text_rect)

        texttroopssurface = myfont.render(troopcount,False,WHITE)#troops
        texttroop_rect = texttroopssurface.get_rect(center = location)
        gameDisplay.blit(texttroopssurface,(texttroop_rect[0],texttroop_rect[1]+20))
        #pygame.draw.rect(gameDisplay,LIGHT_GREEN,(1500,0,WINDOW_WIDTH,WINDOW_HEIGHT))

        ownersurface = myfont.render(owner,False,WHITE)
        owner_rect = ownersurface.get_rect(center = location)
        gameDisplay.blit(ownersurface,(owner_rect[0],owner_rect[1]-20))

    for i in range(1,7):#create players
        playerstextsurface = myfont.render("Player {}".format(i),False,WHITE)
        gameDisplay.blit(playerstextsurface, (1541,(100+(i*100))))
        pygame.draw.circle(gameDisplay,color_dict.get("players").get("Player {}".format(i)),(1650,(100+(i*100))),SMALL_CIRCLE_SIZE)

        player_rects.update({"Player {}".format(i):(1541,(100+(i*100)))}) #need to implement scores of troops and territories on the right

def attack(A,D): #dice rolls
    while True:
        alist = []
        dlist = []
        if A >= 3:
            for i in range(0,3):
                alist.append(random.randint(1,6))
        if A == 2:
            for i in range(0,2):
                alist.append(random.randint(1,6))
        if A == 1:
            for i in range(0,1):
                alist.append(random.randint(1,6))
        if D >= 2:
            for i in range(0,2):
                dlist.append(random.randint(1,6))
        if D == 1:
            for i in range(0,1):
                dlist.append(random.randint(1,6))
        if A == 1:
            break
        if D == 0:
            break
        amax1 = max(alist)
        dmax1 = max(dlist)
        if amax1 > dmax1:
            D -= 1
        if dmax1 >= amax1:
            A -= 1
        if A == 1:
            break
        if D == 0:
            break
        alist.remove(amax1)
        dlist.remove(dmax1)
        if len(alist) > 1:
            amax2 = max(alist)
        if len(alist) == 1:
            amax2 = alist[0]
        if len(dlist) > 1:
            dmax2 = max(dlist)
        elif len(dlist) == 1:
            dmax2 = dlist[0]
        else:
            dmax2 = 0
        if amax2 > dmax2:
            D -= 1
        if dmax2 >= amax2:
            A -= 1

    result = (A,D)
    return result



'''
above this is initializing
below this is while its running
'''
first_click = None
second_click = None
attack_success = False
while not crashed:
    try:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = (pygame.mouse.get_pos())
                    click_x = pos[0]
                    click_y = pos[1]
                    clicked_bool = False
                    for region in NA:
                        x = NA.get(region).get("x")
                        y = NA.get(region).get("y")
                        top = y - CIRCLE_SIZE
                        bottom = y + CIRCLE_SIZE
                        left = x - CIRCLE_SIZE
                        right = x + CIRCLE_SIZE
                        if top <= click_y <= bottom:
                            if left <= click_x <= right:
                                clicked_region = region
                                clicked_bool = True
                                break

                    if clicked_bool == True:
                        if first_click == None:#establish first and second clicks
                            first_click = clicked_region
                        elif second_click == None:
                            second_click = clicked_region
                        #print(clicked_region) #prints deets about the region clicked
                        location = (NA.get(clicked_region).get("x"),NA.get(clicked_region).get("y"))
                        troopcount = str(NA.get(clicked_region).get("troops"))
                        owner = NA.get(clicked_region).get("owner")
                        current_color = (color_dict.get("players").get(NA.get(clicked_region).get("owner")))
                        r,b,g = current_color

                        print(first_click)
                        print(second_click)
                        if first_click != None and second_click != None:#reset the clicks
                            first_connections = (NA.get(first_click).get("connections"))
                            first_owner = NA.get(first_click).get("owner")
                            first_troops = NA.get(first_click).get("troops")
                            second_connections = (NA.get(second_click).get("connections"))
                            second_owner = NA.get(second_click).get("owner")
                            second_troops = NA.get(second_click).get("troops")
                            if first_click in second_connections and second_click in first_connections and first_owner != second_owner and first_troops != 1:#tests to see if an attack is possible
                                print("{} can attack {}".format(first_click,second_click))
                                first_troops,second_troops = attack(first_troops,second_troops)#simulates the dice rolls of the attack
                                print(first_troops,second_troops)
                                if second_troops == 0:#attack was a success
                                    print("success") #need to update it with the proper losses
                                    location = (NA.get(second_click).get("x"),NA.get(second_click).get("y"))
                                    continent_color = color_dict.get("regions").get(NA.get(second_click).get("region"))
                                    pygame.draw.circle(gameDisplay,continent_color,location,CIRCLE_SIZE)
                                    player_color = color_dict.get("players").get(NA.get(first_click).get("owner"))

                                    pygame.draw.circle(gameDisplay,player_color,location,SMALL_CIRCLE_SIZE)

                                    textsurface = myfont.render(second_click, False, WHITE)#country name
                                    text_rect = textsurface.get_rect(center=location)
                                    gameDisplay.blit(textsurface, text_rect)

                                    texttroopssurface = myfont.render(str(second_troops+1),False,WHITE)#troops
                                    texttroop_rect = texttroopssurface.get_rect(center = location)
                                    gameDisplay.blit(texttroopssurface,(texttroop_rect[0],texttroop_rect[1]+20))

                                    ownersurface = myfont.render(first_owner,False,WHITE)
                                    owner_rect = ownersurface.get_rect(center = location)
                                    gameDisplay.blit(ownersurface,(owner_rect[0],owner_rect[1]-20))
                                    #above is updating the new region below is updating the first region
                                    location = (NA.get(first_click).get("x"),NA.get(first_click).get("y"))
                                    continent_color = color_dict.get("regions").get(NA.get(first_click).get("region"))
                                    pygame.draw.circle(gameDisplay,continent_color,location,CIRCLE_SIZE)
                                    player_color = color_dict.get("players").get(NA.get(first_click).get("owner"))

                                    pygame.draw.circle(gameDisplay,player_color,location,SMALL_CIRCLE_SIZE)

                                    textsurface = myfont.render(first_click, False, WHITE)#country name
                                    text_rect = textsurface.get_rect(center=location)
                                    gameDisplay.blit(textsurface, text_rect)

                                    texttroopssurface = myfont.render(str(first_troops-1),False,WHITE)#troops
                                    texttroop_rect = texttroopssurface.get_rect(center = location)
                                    gameDisplay.blit(texttroopssurface,(texttroop_rect[0],texttroop_rect[1]+20))

                                    ownersurface = myfont.render(first_owner,False,WHITE)
                                    owner_rect = ownersurface.get_rect(center = location)
                                    gameDisplay.blit(ownersurface,(owner_rect[0],owner_rect[1]-20))
                                    #below is the white circle in the bottom
                                    troop_button_location = (70,830)
                                    pygame.draw.circle(gameDisplay,WHITE,troop_button_location,CIRCLE_SIZE+20)
                                    texttroopstomove = myfont.render(str(first_troops),False,DEAD_COLOR)
                                    texttrooptomove_rect = texttroopstomove.get_rect(center = troop_button_location)
                                    gameDisplay.blit(texttroopstomove,texttrooptomove_rect)

                                    texttomove = myfont.render("Troops to move",False,DEAD_COLOR)
                                    texttomove_rect = texttomove.get_rect(center = troop_button_location)
                                    gameDisplay.blit(texttomove,(texttomove_rect[0],texttomove_rect[1]-20))

                                    text_press_ctrl = myfont.render("'ctrl' to finish",False,DEAD_COLOR)
                                    text_press_rect = text_press_ctrl.get_rect(center = troop_button_location)
                                    gameDisplay.blit(text_press_ctrl,(text_press_rect[0],text_press_rect[1]+35))

                                    troops_to_allocate = first_troops
                                    total_possible_troops = first_troops
                                    NA.get(first_click).update({"troops":first_troops-1})
                                    NA.get(second_click).update({"troops":second_troops+1})
                                    attack_success = True
                                    decided = False
                                    pygame.display.update()
                                else:
                                    attack_success = False
                                    first_click = None
                                    second_click = None
                                if attack_success == True:
                                    pass
                            else:
                                print("{} can not attack {}".format(first_click,second_click))

                    if clicked_bool == False:
                        print("No region clicked")
                        print(pos)
            if attack_success == True:
                while decided == False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 4: #need to change this so 3 is possible. Scroll up. advance
                                troops_to_allocate += 1
                                first_troops -= 1
                                if troops_to_allocate >= total_possible_troops:
                                    troops_to_allocate = total_possible_troops-1
                                    first_troops = 1
                            if event.button == 5: #scroll down. retreat
                                troops_to_allocate -= 1
                                first_troops += 1
                                if troops_to_allocate <= 1 or first_troops >= total_possible_troops:
                                    troops_to_allocate = 1
                                    first_troops = total_possible_troops-1

                            location = (NA.get(second_click).get("x"),NA.get(second_click).get("y"))

                            pygame.draw.circle(gameDisplay,WHITE,troop_button_location,CIRCLE_SIZE+20)
                            texttroopstomove = myfont.render(str(troops_to_allocate),False,DEAD_COLOR)
                            texttrooptomove_rect = texttroopstomove.get_rect(center = troop_button_location)
                            gameDisplay.blit(texttroopstomove,texttrooptomove_rect)

                            continent_color = color_dict.get("regions").get(NA.get(second_click).get("region"))#continent circle
                            pygame.draw.circle(gameDisplay,continent_color,location,CIRCLE_SIZE)

                            player_color = color_dict.get("players").get(NA.get(first_click).get("owner"))#player color
                            pygame.draw.circle(gameDisplay,player_color,location,SMALL_CIRCLE_SIZE)

                            textsurface = myfont.render(second_click, False, WHITE)#country name
                            text_rect = textsurface.get_rect(center=location)
                            gameDisplay.blit(textsurface, text_rect)

                            ownersurface = myfont.render(first_owner,False,WHITE)
                            owner_rect = ownersurface.get_rect(center = location)
                            gameDisplay.blit(ownersurface,(owner_rect[0],owner_rect[1]-20))

                            texttroopssurface = myfont.render(str(troops_to_allocate),False,WHITE)#troops in newly aquired region
                            texttroop_rect = texttroopssurface.get_rect(center = location)
                            gameDisplay.blit(texttroopssurface,(texttroop_rect[0],texttroop_rect[1]+20))

                            texttomove = myfont.render("Troops to move",False,DEAD_COLOR)
                            texttomove_rect = texttomove.get_rect(center = troop_button_location)
                            gameDisplay.blit(texttomove,(texttomove_rect[0],texttomove_rect[1]-20))
                            #above is for the new territory. below is for the existing territory
                            location = (NA.get(first_click).get("x"),NA.get(first_click).get("y"))

                            continent_color = color_dict.get("regions").get(NA.get(second_click).get("region"))#continent circle
                            pygame.draw.circle(gameDisplay,continent_color,location,CIRCLE_SIZE)

                            player_color = color_dict.get("players").get(NA.get(first_click).get("owner"))#player color
                            pygame.draw.circle(gameDisplay,player_color,location,SMALL_CIRCLE_SIZE)

                            textsurface = myfont.render(first_click, False, WHITE)#country name
                            text_rect = textsurface.get_rect(center=location)
                            gameDisplay.blit(textsurface, text_rect)

                            ownersurface = myfont.render(first_owner,False,WHITE)
                            owner_rect = ownersurface.get_rect(center = location)
                            gameDisplay.blit(ownersurface,(owner_rect[0],owner_rect[1]-20))

                            texttroopssurface = myfont.render(str(first_troops),False,WHITE)#troops in newly aquired region
                            texttroop_rect = texttroopssurface.get_rect(center = location)
                            gameDisplay.blit(texttroopssurface,(texttroop_rect[0],texttroop_rect[1]+20))


                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LCTRL:
                                pygame.draw.circle(gameDisplay,DEAD_COLOR,troop_button_location,CIRCLE_SIZE+20)#removes the white circle
                                NA.get(first_click).update({"owner":first_owner})
                                NA.get(first_click).update({"troops":first_troops})
                                NA.get(second_click).update({"owner":first_owner})
                                NA.get(second_click).update({"troops":troops_to_allocate}) #update the db
                                first_click = None
                                second_click = None
                                decided = True

                        pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    crashed = True

        pygame.display.update()
    except KeyboardInterrupt:
        break

pygame.quit()
quit()
