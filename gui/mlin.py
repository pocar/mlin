#!/usr/bin/python
'''
Created on 5. avg. 2012

@author: anton
'''

import pygame
from pygame.locals import *
from igralnadeska import IgralnaDeska
from gradniki import *

velikostZaslona = [640, 480]

bela = (255, 255, 255)
crna = (0,   0,   0  )
svetlo_siva = (230, 230, 230)
temno_siva = (80, 80, 80)



def main():
    pygame.init() #@UndefinedVariable
    
    deska = IgralnaDeska(Rect((0,0),(velikostZaslona[0],velikostZaslona[1]-60)))
    statusnaVrstica = StatusnaVrstica(Rect([0, velikostZaslona[1]-25, velikostZaslona[0], 25]))
    novaIgra = Gumb(Rect([0, velikostZaslona[1]-57, velikostZaslona[0]//3, 30]), "Nova igra")
    
#    for i in range(24):
#        deska.polje[i].zeton = 1 + (i % 2)
#        print("{0} -> {1}".format(i,deska.polje[i].center))    
    
    zaslon = pygame.display.set_mode(velikostZaslona)
    
    pygame.display.set_caption("Mlin")

    clock = pygame.time.Clock()
    done = False
    while done == False:
        # event handling
        for event in pygame.event.get(): # User did something
            if event.type == MOUSEBUTTONDOWN: #@UndefinedVariable
                if deska.konecIgre == False:
                    deska.klikDol(event)
                novaIgra.klikDol(event)
            elif event.type == MOUSEBUTTONUP: #@UndefinedVariable
                if deska.konecIgre == False:
                    deska.klikGor(event)
                novaIgra.klikGor(event)
            elif event.type == QUIT: # If user clicked close @UndefinedVariable
                done=True # Flag that we are done so we exit this loop

        # posodobitev stanja gradnikov
        statusnaVrstica.status(deska.status())
        # izrisovanje
        zaslon.fill(bela)
        deska.izrisiDesko(zaslon)
        statusnaVrstica.izrisi(zaslon)
        novaIgra.izrisi(zaslon)
        # izpiši status
        # update the zaslon
        pygame.display.flip()
        # wait till next frame
        clock.tick(30)
    pygame.quit() #@UndefinedVariable

if __name__ == '__main__':
    main()