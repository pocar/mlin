'''
Created on 9. avg. 2012

@author: anton
'''

import pygame

class StatusnaVrstica(object):
    '''
    classdocs
    '''
    ospredje = (0, 0, 0)
    ozadje = (255, 255, 255)

    def __init__(self, velikost):
        '''
        velikost: pygame.Rect
        '''
        self.okvir = velikost
        self.pisava = pygame.font.Font(None,int(velikost.h*0.9))
        self.vsebina = ''
        self.izhodisceBesedila = (velikost.x + 5, velikost.y + int(0.2*velikost.h))
    
    def status(self, besedilo):
        self.vsebina = besedilo
        
    def izrisi(self, platno):
        pygame.draw.line(platno, self.ospredje, self.okvir.topleft, self.okvir.topright)
        napis = self.pisava.render(self.vsebina, True, self.ospredje)
        napisOkvir = napis.get_rect()
        napisOkvir.topleft = self.izhodisceBesedila
        platno.blit(napis,napisOkvir)



        
class Gumb(object):
    '''
        Gumb
    '''
    crna = (0, 0, 0)
    temno_zelena = (0, 158, 0)
    svetlo_siva = (192, 192, 192)
    temno_siva = (80, 80, 80)
    
    def __init__(self,okvir, napis):
        self.napis = napis        
        self.okvir = okvir
        # zmanjšamo višino in širino za ena
        self.okvir.h -= 2
        self.okvir.w -= 2
        self.spodnjiOkvir = self.okvir.move(2, 2)
        print("okvir = {0}, spodnjiOkvir = {1}".format(self.okvir,self.spodnjiOkvir))
        self.pisava = pygame.font.Font(None,20)
        self.pritisnjen = False
        self.nastaviKlicnoFunkcijo(None, None)
    
    def nastaviKlicnoFunkcijo(self, klicnaFunk, parameter):
        self.klicnaFunk = klicnaFunk
        self.parameter = parameter
    
    def klikDol(self, event):
        self.pritisnjen = self.okvir.collidepoint(event.pos)
    
    def klikGor(self, event):
        if self.pritisnjen and self.okvir.collidepoint(event.pos):
            if self.klicnaFunk is not None:
                self.klicnaFunk(self.parameter)
        self.pritisnjen = False
    
    def izrisi(self, platno):
        if self.pritisnjen:
            pygame.draw.rect(platno, self.temno_zelena, self.spodnjiOkvir, 0)
            pygame.draw.rect(platno, self.temno_siva, self.spodnjiOkvir, 1)
            napis = self.pisava.render(self.napis, True, self.crna)
            napisOkvir = napis.get_rect()
            napisOkvir.center = self.spodnjiOkvir.center
            platno.blit(napis, napisOkvir)
        else:
            pygame.draw.rect(platno, self.svetlo_siva, self.spodnjiOkvir, 0)
            pygame.draw.rect(platno, self.temno_zelena, self.okvir, 0)
            pygame.draw.rect(platno, self.temno_siva, self.okvir, 1)
            napis = self.pisava.render(self.napis, True, self.crna)
            napisOkvir = napis.get_rect()
            napisOkvir.center = self.okvir.center
            platno.blit(napis, napisOkvir)
