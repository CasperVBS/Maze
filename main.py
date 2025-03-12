import pygame 
import time
import kleur
import random
import art
from config import *
from colorama import Fore
import os
from screeninfo import get_monitors


start_time = time.time() 

print(Fore.GREEN,"")

monitors = get_monitors()
if len(monitors) == 1:
    monitor = monitors[0]
if len(monitors) == 3:
    monitor = monitors[1]
monitor_x = monitor.x 
monitor_y = monitor.y  # y-coördinaat van de tweede monitor
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_x + 25 },{monitor_y + 25}"


print(art.text2art("Maze Generator"))
print(art.text2art("Casper Vanbeselaere"))
random.randint(0,3) 
 
pygame.init() 






#berekenen hoe groot ik mijn scherm moet instellen
x_scherm = kolomen*(groote_vakjes)+(kolomen+2)*lijndikte
y_scherm = rijen*(groote_vakjes)+(rijen+2)*lijndikte
Berekende_grote_scherm = [x_scherm,y_scherm]
#TODO manier om de grote van de vakjes aan tepassen aan de resolutie van de gebruikers scherm
res_scherm = pygame.display.get_desktop_sizes()[0] #eerste scherm gebruiken 
(x_res_scherm,y_res_scherm) = res_scherm
x_res_scherm -= 120
y_res_scherm -= 120
print(res_scherm)
print(f"Breete van het scherm: {x_res_scherm}\n"
    f"hoogte van het scherm: {y_res_scherm}")

persentage_groote = 1.00
persentage_x = 1.00
persentage_y = 1.00
if x_scherm > x_res_scherm:
    persentage_x = x_res_scherm / x_scherm
if y_scherm > y_res_scherm:
    persentage_y = y_res_scherm / y_scherm
if persentage_x < persentage_y:
    persentage_groote = persentage_x
else:
    persentage_groote = persentage_y

groote_scherm = []
groote_vakjes *= persentage_groote
lijndikte *= persentage_groote
for element in Berekende_grote_scherm:
    element *= persentage_groote 
    groote_scherm.append(element)





screen = pygame.display.set_mode(groote_scherm)
pygame.display.set_caption("Casper Vanbeselaere Doolhof")
screen.fill(achtergrond_kleur)
pygame.display.set_icon(pygame.image.load("imgs/maze.jpg"))
pygame.display.flip()


# images for derections 
pijl = pygame.image.load("imgs/pijl.png")
pijl = pygame.transform.scale(pijl,(groote_vakjes + lijndikte/kolomen,groote_vakjes + lijndikte/rijen))
pijl = pygame.transform.rotate(pijl,-90)
arrow_up = pygame.transform.rotate(pijl,180)
arrow_right = pygame.transform.rotate(pijl,90)
arrow_down = pygame.transform.rotate(pijl,0)
arrow_left = pygame.transform.rotate(pijl,270)


cirkel = pygame.image.load("imgs/cirkel.png")
cirkel = pygame.transform.scale(cirkel,(groote_vakjes + lijndikte/kolomen,groote_vakjes + lijndikte/rijen))

player = pygame.image.load("imgs/player.png")
player = pygame.transform.scale(player,(groote_vakjes + lijndikte/kolomen, groote_vakjes + lijndikte / rijen))

Gewonnen_img = pygame.image.load("imgs\gewonnen.jpg")
Gewonnen_img = pygame.transform.scale(Gewonnen_img,groote_scherm)
def animeer(t):
    time.sleep(0)
    pygame.display.flip()

def Teken_grid(animatie_opbouw_local=animatie_opbouw):
    #pygame.Rect(x,y,lengte,breete)
    for kolom in range(kolomen+1):
        x = (groote_scherm[0]- lijndikte)/(kolomen)*(kolom)
        pygame.draw.rect(screen,(kleur.Light_Lime),pygame.Rect(x,0,lijndikte,groote_scherm[1]))
        if animatie_opbouw_local: animeer(0.01)



    for rij in range(rijen+1):
        y = (groote_scherm[1]-lijndikte )/(rijen)*(rij)
        pygame.draw.rect(screen,kleur.Light_Lime,pygame.Rect(0,y,groote_scherm[0],lijndikte))
        if animatie_opbouw_local: animeer(0.01)


# lijst cell met elke cel de lijst krijgt: [x_center,y_center]
# TODO KLOPT NOG NIET HELEMAAL
# UPDATE: te veel problemen met centrum => geen centrum maar linker boven hoek (zonder lijndikte
cellen = []
for rij in range(rijen):
    y = (lijndikte + (groote_vakjes+(lijndikte/rijen)))*rij + lijndikte  
    for kolom in range(kolomen):
        x = (lijndikte + groote_vakjes + (lijndikte/kolomen))*kolom + lijndikte 
        tijdelijke_cel = [x,y]
        cellen.append(tijdelijke_cel)






Teken_grid()
#pygame.Rect(x,y,lengte,breete)
for cel in cellen:
    pygame.draw.rect(screen,kleur.green,pygame.Rect(cel[0] ,cel[1],1,1))


def Kleur_cel(cel_nummer,animatie_opbouw_local=animatie_opbouw, kleur = achtergrond_kleur):
    cel_waarden = cellen[cel_nummer]
    x,y = cellen[cel_nummer]
    x_grote = groote_vakjes + lijndikte/kolomen
    y_grote = groote_vakjes + lijndikte/rijen
    pygame.draw.rect(screen,kleur,pygame.Rect(x, y,x_grote,y_grote))
    if animatie_opbouw_local: animeer(0.01)

def kleur_alle_cellen():    
    for i in range(int(len(cellen))):
        Kleur_cel(i,False)    



# zogrd dat we de cellen kunnen aanspreken via coordinaten 
def grid_to_cels(cordinate):
    x,y = cordinate
    cel = y*kolomen + x
    return cel

def cels_to_grid(cel):
    y = cel // kolomen
    x = cel % kolomen
    return (x,y)

#print(cel)

# kleur_alle_cellen()


def toon_derection(cel, direction):
    x , y = cellen[cel]
    if direction == 0:
        screen.blit(arrow_up,(x,y))
    elif direction == 1:
        screen.blit(arrow_right,(x,y))
    elif direction == 2:
        screen.blit(arrow_down,(x,y))
    elif direction == 3:
        screen.blit(arrow_left,(x,y))


#pygame.Rect(x,y,lengte,breete)
def omkader_cel(cel,derection, einde = False):
    dementie_x = groote_vakjes + 2*lijndikte + lijndikte/kolomen
    dementie_y = groote_vakjes + 2*lijndikte + lijndikte/rijen
    x_grid, y_grid = cels_to_grid(cel)
    x = x_grid*((groote_vakjes + lijndikte/kolomen)+lijndikte)
    y = y_grid*(groote_vakjes+lijndikte + lijndikte/rijen) 
    y_onder = y + groote_vakjes + lijndikte/rijen + lijndikte
    x_rechts = x + groote_vakjes + lijndikte/kolomen + lijndikte
    if einde == False:
        # omkader alle randen in rood
        pygame.draw.rect(screen,Kleur_maze,pygame.Rect(x,y,dementie_x,lijndikte))
        pygame.draw.rect(screen,Kleur_maze,pygame.Rect(x,y,lijndikte,dementie_y))
        pygame.draw.rect(screen,Kleur_maze,pygame.Rect(x,y_onder ,dementie_x,lijndikte))
        pygame.draw.rect(screen,Kleur_maze,pygame.Rect(x_rechts,y,lijndikte,dementie_y))

    # verwijderen van muur (door middel van kleur achtergrond te maken)
    if derection == 0:
        x += lijndikte
        dementie_x -= 2* lijndikte
        pygame.draw.rect(screen,achtergrond_kleur,pygame.Rect(x,y_onder ,dementie_x ,lijndikte))
    elif derection == 1:
        y += lijndikte
        dementie_y -= 2* lijndikte
        pygame.draw.rect(screen,achtergrond_kleur,pygame.Rect(x,y,lijndikte,dementie_y))
    elif derection == 2:
        x += lijndikte
        dementie_x -= 2*lijndikte
        pygame.draw.rect(screen,achtergrond_kleur,pygame.Rect(x,y,dementie_x,lijndikte))
    elif derection == 3:
        y += lijndikte
        dementie_y -= 2* lijndikte
        pygame.draw.rect(screen,achtergrond_kleur,pygame.Rect(x_rechts,y,lijndikte,dementie_y))
    elif derection == 4:
        pass 
        # zorgt voor dat eerste cel voledig is omkadert
    else:
        print(f"Error: {derection} is geen mogelijke invoerwaarde ")
    if animatie_opbouw: animeer(0.00004)

    
def einde(random_place = True,x=0,y=0):
    if random_place:
        rij_of_kolom = random.randint(1,2)
        if rij_of_kolom == 1:
            rij = random.choice([0,rijen-1])
            kolom = random.randint(0,kolomen-1)
        elif rij_of_kolom == 2:
            rij = random.randint(0,rijen-1)
            kolom = random.choice([0,kolomen-1])
    else:
        pass
    x = kolom
    y = rij
    if x == kolomen -1:
        derection = 3
    elif x == 0:
        derection = 1
    elif y == rijen - 1:
        derection = 0
    elif y == 0:
        derection = 2    
    omkader_cel(grid_to_cels((kolom,rij)),derection, True)
    if debug:   
        x_eind , y_eind = cellen[grid_to_cels((kolom,rij))]
        screen.blit(cirkel,(x_eind,y_eind))
    eind_cel = grid_to_cels((kolom,rij))
    return eind_cel
    





running = True

visited_cels = []
Path = []
Path_nav = []
max_beurten = 100

is_gedaan = False


    

start = (2,0)
plaats = start
Kleur_cel(grid_to_cels(plaats))
omkader_cel(grid_to_cels(plaats), 5)
cel_start = grid_to_cels(start)
x_start , y_start = cellen[cel_start]
screen.blit(cirkel,(x_start,y_start))
visited_cels.append(cel_start)

while is_gedaan == False:
    beurt = 1

    mogelijkheden = []
    x_plaats, y_plaats = plaats
    if y_plaats > 0 and grid_to_cels((x_plaats,y_plaats - 1)) not in visited_cels:
        mogelijkheden.append(0)
    if x_plaats < kolomen - 1 and grid_to_cels((x_plaats + 1, y_plaats)) not in visited_cels:
        mogelijkheden.append(1)
    if y_plaats < rijen - 1 and grid_to_cels((x_plaats,y_plaats + 1)) not in visited_cels:
        mogelijkheden.append(2)
    if x_plaats > 0 and grid_to_cels((x_plaats - 1, y_plaats)) not in visited_cels:
        mogelijkheden.append(3)
    
    if not mogelijkheden == []:
        derection = random.choice(mogelijkheden)
        # up
        if derection == 0:
            if debug:    print("up")
            y_plaats -= 1
        # right
        elif derection == 1:
            if debug:   print("right")
            x_plaats += 1
        # down
        elif derection == 2:
            if debug:   print("down")
            y_plaats += 1
        # left
        elif derection == 3:
            if debug:    print("left")
            x_plaats -= 1

        plaats = (x_plaats,y_plaats)
        cel_plaats = grid_to_cels(plaats)
        visited_cels.append(cel_plaats)
        Path.append(cel_plaats)
        Path_nav.append(cel_plaats) 
        

        beurt += 1 
        
        omkader_cel(grid_to_cels(plaats),derection)
    else:
        #GEEN MOGELIJK HEID => terug keren 
        geslaagd = True
        if Path_nav:
            plaats  = cels_to_grid(Path_nav.pop())
            if debug: 
                print(Path_nav)
        else:
            geslaagd = True
            is_gedaan = True



end_time = time.time() 
execution_time = end_time - start_time
naam = f"imgs/mazes/Maze {kolomen} x {rijen} , {round(execution_time,2)}s.png"
pygame.image.save(screen,naam)





# Solver

def doorgang(cel,derection): 
    x , y = cellen[cel]
    x = int(x - 1/2 * lijndikte)
    y = int(y -1/2 * lijndikte)
    # up
    if derection == 0:
        x = x + lijndikte *1/2 + groote_vakjes *1/2
    # right
    elif derection == 1:
        x += groote_vakjes + lijndikte/ kolomen + lijndikte
        y += lijndikte * 1/2 + groote_vakjes *1/2
    # down
    elif derection == 2: 
        x += (lijndikte + groote_vakjes) * 1/2
        y += groote_vakjes + lijndikte / rijen + lijndikte
    # left
    elif derection == 3:
        y += (lijndikte + groote_vakjes) * 1/2
    kleur_muur = screen.get_at((int(x-1),int(y-1)))[:3]
    if debug:
        pygame.draw.rect(screen,kleur.Black,pygame.Rect(x,y,10,10))
    if kleur_muur == Kleur_maze:
        return False
    else:
        return True
    

def kleur_path(cel):
    x,y = cellen[cel]
    x_dementie = groote_vakjes + lijndikte/kolomen
    y_dementie = groote_vakjes + lijndikte/rijen
    pygame.draw.rect(screen,kleur.Gold,pygame.Rect(x,y,x_dementie,y_dementie ))


start = cels_to_grid(cel_start)



eind_cel = einde()

plaatsen_speler = [start]
end_maze_move = False

def move_speler(derection):
    mogelijkheden = []
    plaats_speler = plaatsen_speler[-1]
    x_player = plaats_speler[0]
    y_player = plaats_speler[1]
    plaats = grid_to_cels(plaats_speler)
    # verwijder oude plaats van speler
    dementie_x = groote_vakjes + lijndikte/kolomen
    dementie_y = groote_vakjes + lijndikte/rijen
    x_coordinaat, y_coordinaat = cellen[plaats]
    pygame.draw.rect(screen,achtergrond_kleur,pygame.Rect(x_coordinaat,y_coordinaat,dementie_x,dementie_y))
    pygame.display.flip()
    if doorgang(plaats,0):
        mogelijkheden.append(0)
    if doorgang(plaats,1):
        mogelijkheden.append(1)
    if doorgang(plaats,2):
        mogelijkheden.append(2)
    if doorgang(plaats,3):
        mogelijkheden.append(3)
      
    

    if derection in mogelijkheden:
        if derection == 0:
            y_player -= 1
        if derection == 1:
            x_player += 1
        if derection == 2:
            y_player += 1
        if derection == 3:
            x_player -= 1
    else: 
        if debug:
            print(f"{derection} is niet mogelijk")
    nieuwe_plaats = grid_to_cels((x_player,y_player))
    plaatsen_speler.append((x_player,y_player))
    if nieuwe_plaats == eind_cel:
        print("gewonnen")
        end_maze_move = True
        screen.blit(Gewonnen_img,(0,0))
    else:
        x_coordinaat, y_coordinaat = cellen[nieuwe_plaats]
        screen.blit(player,(x_coordinaat,y_coordinaat))




while running:
    for event in pygame.event.get(): 
                    
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_z or event.key == pygame.K_UP:
                move_speler(0)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_speler(1)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                move_speler(2)
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                move_speler(3)

            pygame.display.update()


