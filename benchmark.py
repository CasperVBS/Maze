import pygame 
import time
import kleur
import random
import art

import os
from screeninfo import get_monitors

for i in range(100):

    start_time = time.time() 

    kolomen = i + 102
    rijen = i + 102
    groote_vakjes = 100
    lijndikte = 25
    animatie_opbouw = False

    monitors = get_monitors()
    if len(monitors) == 1:
        monitor = monitors[0]
    if len(monitors) == 3:
        monitor = monitors[1]
    monitor_x = monitor.x # x-coördinaat van de tweede monitor
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
    x_res_scherm += 20
    y_res_scherm += 20
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
    screen.fill(kleur.achtergrondkleur)
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

    def animeer(t):
        time.sleep(t)
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
        pygame.draw.rect(screen,(250,0,0),pygame.Rect(cel[0] ,cel[1],1,1))


    def Kleur_cel(cel_nummer,animatie_opbouw_local=animatie_opbouw):
        cel_waarden = cellen[cel_nummer]
        x,y = cellen[cel_nummer]
        x_grote = groote_vakjes + lijndikte/kolomen
        y_grote = groote_vakjes + lijndikte/rijen
        pygame.draw.rect(screen,kleur.Navy,pygame.Rect(x, y,x_grote,y_grote))
        if animatie_opbouw_local: animeer(0.01)

    def kleur_alle_cellen():    
        for i in range(int(len(cellen))):
            Kleur_cel(i)    



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
    def omkader_cel(cel,derection):
        dementie_x = groote_vakjes + 2*lijndikte + lijndikte/kolomen
        dementie_y = groote_vakjes + 2*lijndikte + lijndikte/rijen
        x_grid, y_grid = cels_to_grid(cel)
        x = x_grid*((groote_vakjes + lijndikte/kolomen)+lijndikte)
        y = y_grid*(groote_vakjes+lijndikte + lijndikte/rijen) 
        y_onder = y + groote_vakjes + lijndikte/rijen + lijndikte
        x_rechts = x + groote_vakjes + lijndikte/kolomen + lijndikte

        # omkader alle randen in rood
        pygame.draw.rect(screen,kleur.Red,pygame.Rect(x,y,dementie_x,lijndikte))
        pygame.draw.rect(screen,kleur.Red,pygame.Rect(x,y,lijndikte,dementie_y))
        pygame.draw.rect(screen,kleur.Red,pygame.Rect(x,y_onder ,dementie_x,lijndikte))
        pygame.draw.rect(screen,kleur.Red,pygame.Rect(x_rechts,y,lijndikte,dementie_y))

        # verwijderen van muur (door middel van kleur achtergrond te maken)
        if derection == 0:
            x += lijndikte
            dementie_x -= 2* lijndikte
            pygame.draw.rect(screen,kleur.achtergrondkleur,pygame.Rect(x,y_onder ,dementie_x ,lijndikte))
        elif derection == 3:
            y += lijndikte
            dementie_y -= 2* lijndikte
            pygame.draw.rect(screen,kleur.achtergrondkleur,pygame.Rect(x_rechts,y,lijndikte,dementie_y))
        elif derection == 2:
            x += lijndikte
            dementie_x -= 2*lijndikte
            pygame.draw.rect(screen,kleur.achtergrondkleur,pygame.Rect(x,y,dementie_x,lijndikte))
        elif derection == 1:
            y += lijndikte
            dementie_y -= 2* lijndikte
            pygame.draw.rect(screen,kleur.achtergrondkleur,pygame.Rect(x,y,lijndikte,dementie_y))
        elif derection == 5:
            pass
        else:
            print(f"Error: {derection} is geen mogelijke invoerwaarde ")
        if animatie_opbouw: animeer(0.5)

        





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
                print("up")
                y_plaats -= 1
            # right
            elif derection == 1:
                print("right")
                x_plaats += 1
            # down
            elif derection == 2:
                print("down")
                y_plaats += 1
            # left
            elif derection == 3:
                print("left")
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
                print(Path_nav)
            else:
                geslaagd = True
                is_gedaan = True

    end_time = time.time() 
    execution_time = end_time - start_time
    naam = f"imgs/mazes/Maze {kolomen} x {rijen} , {round(execution_time,2)}s.png"
    pygame.image.save(screen,naam)

    #print(cellen)
    #print(dict_derection)
    #print(cel_dict)
    #print(Path)
    while running:
        
        for event in pygame.event.get(): 

                
            if event.type == pygame.QUIT: 
                running = False
            pygame.display.update()
        
        pygame.display.flip()
        running = False

