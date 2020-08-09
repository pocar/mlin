'''
Created on 5. avg. 2012

@author: anton
'''

import pygame

bela = (255, 255, 255)
crna = (0,   0,   0  )
svetlo_siva = (230, 230, 230)
temno_siva = (80, 80, 80)

class Polje(object):
    ''' Predstavlja polje, kamor se lahko odloži žeton'''

    
    def __init__(self, oznaka = None, polmer = 0, zeton = None):
        ''' zeton je referenca na igralca, kateremu pripada žeton na tem mestu '''
        self.oznaka = oznaka
        self.polmer = polmer
        # 0 predstavlja prosto polje
        self.zeton = zeton
        self.center = (0, 0)
        # sosednja polja
        self.levo = None
        self.desno = None
        self.gor = None
        self.dol = None
        
    
    def znotraj(self, pozicija):
        x1, y1 = self.center
        x2, y2 = pozicija
        return ( ((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)) <= self.polmer*self.polmer )

    def delTrojke(self):
        ''' preveri, če je polje vključeno v vrsto treh enakih žetonov
            -> vrne n-terico polj vključenih v vrsto oz. None
        '''
        # najprej v horizontali
        if self.desno is not None and self.desno.zeton == self.zeton:
            # zeton je skrajno desno v vrsti
            if self.desno.desno is not None and self.desno.desno.zeton is self.zeton:
                return (self, self.desno, self.desno.desno)
            # zeton je v sredini vrste
            elif self.levo is not None and self.levo.zeton is self.zeton:
                return (self.levo, self, self.desno)
        elif self.levo is not None and self.levo.zeton == self.zeton:
            # zeton je skarajno levo v vrsti
            if self.levo.levo is not None and self.levo.levo.zeton is self.zeton:
                return (self.levo.levo, self.levo, self)
        # še vertikala
        elif self.gor is not None and self.gor.zeton is self.zeton:
            # zeton je skrajno spodaj v stolpcu
            if self.gor.gor is not None and self.gor.gor.zeton is self.zeton:
                return (self.gor.gor, self.gor, self)
            # zeton je na sredini stolpca
            if self.dol is not None and self.dol.zeton is self.zeton:
                return (self.gor, self, self.dol)
        elif self.dol is not None and self.dol.zeton is self.zeton:
            # zeton je skrajno zgoraj v stolpcu
            if self.dol.dol is not None and self.dol.dol.zeton is self.zeton:
                return (self, self.dol, self.dol.dol)
        return None

    def prosto(self):
        return (self.zeton is None)

    def izprazni(self):
        self.zeton = None

    def sosednjePolje(self, polje):
        return polje in (self.levo, self.desno, self.gor, self.dol)

    def izrisiZeton(self, povrsina, debelinaCrt = 1):
        if self.zeton is not None:
            okvir = pygame.Rect(0,0,self.polmer*2,self.polmer*2)
            okvir.center = self.center
            # najprej narišemo krog
            pygame.draw.ellipse(povrsina, self.zeton.barva, okvir, 0)
            # risanje posameznih kroglic
            for radij in [2*self.polmer, 7*self.polmer//6, 3*self.polmer//2]:
                okvir.size = (radij, radij)
                okvir.center = self.center
                pygame.draw.ellipse(povrsina, crna, okvir, debelinaCrt)


class Igralec(object):
    ''' Stanje in podatki o igralcu '''
    
    def __init__(self,zetonovNaZacetku, barva):
        self.zetonovProstih = zetonovNaZacetku
        self.zetonovNaDeski = 0    
        self.barva = barva
        self.sidrisceProstihZetonov = (0,0)
    
    def zetonNaDesko(self):
        self.zetonovProstih -= 1
        self.zetonovNaDeski += 1

    def zetonVzet(self):
        self.zetonovNaDeski -= 1
    
    def izgubil(self):
        return (self.zetonovProstih + self.zetonovNaDeski) < 3
    
    def izrisiProsteZetone(self, platno, polmerZetona):
        zeton = Polje(None, polmerZetona, self)
        x, y = self.sidrisceProstihZetonov
        y -= polmerZetona
        for i in range(self.zetonovProstih):
            zeton.center = (x, y - i * 2 * polmerZetona)
            zeton.izrisiZeton(platno)

class IgralnaDeska(object):
    '''
    Vse informacije o trenutnem stanju igre
    '''

    def __init__(self, velikostZaslona):
        '''
        Inicializira notranje stanje igralne deske
        '''
        oznake_polj = [ 'a1', 'a4', 'a7', 'b2', 'b4', 'b6', 'c3', 'c4', 'c5', 
                       'd1', 'd2', 'd3', 'd5', 'd6', 'd7',
                       'e3', 'e4', 'e5', 'f2', 'f4', 'f6', 'g1', 'g4', 'g7']
        self.polje = [Polje(oznaka) for oznaka in oznake_polj]
        # pravilno poveži polja
        # polja so oštevilčena od leve proti desni, od gor navzdol
        # najprej povezava vse, ki imajo desne sosede
        for i in range(23):
            if (i % 3) != 2: # ima desnega soseda
                self.polje[i].desno = self.polje[i+1]
                self.polje[i+1].levo = self.polje[i]
        # še povezave gor-dol s kotnimi polji        
        for i, pl in enumerate([0, 3, 6]):
            self.polje[pl].dol = self.polje[9+i]
            self.polje[9+i].gor = self.polje[pl]
        for i, pl in enumerate([8, 5, 2]):
            self.polje[pl].dol = self.polje[12+i]
            self.polje[12+i].gor = self.polje[pl]
        for i, pl in enumerate([21, 18, 15]):
            self.polje[pl].gor = self.polje[9+i]
            self.polje[9+i].dol = self.polje[pl]
        for i, pl in enumerate([17, 20, 23]):
            self.polje[pl].gor = self.polje[12+i]
            self.polje[12+i].dol = self.polje[pl]
        # povezave gor-dol s sredinskimi polji
        for i in [1, 4, 16, 19]:
            self.polje[i].dol = self.polje[i+3]
            self.polje[i+3].gor = self.polje[i]
        # stanje igralcev
        self.naPotezi = 1
        self.igralec = [Igralec(9, svetlo_siva), Igralec(9, temno_siva)]
        self.stadijIgre = 'POLAGANJE/PREMIKANJE'        
        # animacija premikanja zetona
        self.lebdeciZeton = Polje('lebdeci')
        self.izvornoPolje = None
        self.miskinGumbDol = False
        # konec igre
        self.konecIgre = False
        # opis stanja
        self.opisStanja = "Igralec 1 na potezi ..."
        # irazcuanj se dimenzije za izris deske
        self.preracunajDimenzije(velikostZaslona)
    
    def preracunajDimenzije(self, zaslonVelk):
        # sirina polja
        obstrani = 2.8
        self.razmak = int(zaslonVelk.w / (6+2*obstrani))
        self.deska = zaslonVelk.inflate(-int(2*obstrani*self.razmak),0)
        # obrezi v kvadrat
        sirina, visina = self.deska.size
        if sirina < visina:
            self.deska.inflate_ip(0,sirina - visina)
        else:
            self.deska.inflate_ip(visina - sirina, 0)
        # spravi koordinate možnih odložišč žetonov v sezanm
        robx, roby = self.deska.topleft
        sirina, visina = self.deska.size
        korak = 3 #* self.razmak # razmik med vodoravnimi polji
        self.polmerPolja = int(self.razmak * 8 / 20)
        pl = 0 # indeks polja
        # zgornja polja
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                self.polje[pl].center = (robx+((i+j*korak)*sirina/6), roby+int(i*visina/6))
                self.polje[pl].polmer = self.polmerPolja
                pl += 1
            # zamanjšamo še razmak med polji
            korak -= 1 #self.razmak
        # polja na sredini (od leve do desne)
        roby += sirina // 2#3*self.razmak
        korak = 1 #self.razmak
        for i in [0, 1, 2, 4, 5, 6]:
            self.polje[pl].center = (robx+int(i*korak*sirina/6), roby)
            self.polje[pl].polmer = self.polmerPolja
            pl += 1
        # spodnja polja
        roby = self.deska.y + int(4*visina/6)
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                self.polje[pl].center = (robx+((2-i+j*korak)*sirina/6), roby+int(i*visina/6))
                self.polje[pl].polmer = self.polmerPolja
                pl += 1
                # zamanjšamo še razmak med polji
            korak += 1 #self.razmak
        # nastavi polmer žetona še lebdečeu žetonu
        self.lebdeciZeton.polmer = self.polmerPolja
        # izračunaj, kaj naj se postavijo prosti žetoni
        rob = int((obstrani/2) * self.razmak)
        self.igralec[0].sidrisceProstihZetonov = (rob, zaslonVelk.h )
        self.igralec[1].sidrisceProstihZetonov = (zaslonVelk.w - rob, zaslonVelk.h)

    def poljeNaPoziciji(self, pozicija):
        for polje in self.polje:
            if polje.znotraj(pozicija):
                return polje
        return None

    def zetonDovoljenoVzeti(self, ciljnoPolje, nasprotnik):
        # če nismo kliknili nasprotnikovega žetona, spodleti
        if ciljnoPolje.zeton != nasprotnik:
            return False
        # če lahko vzamemo žeton, ki ni del trojke, prepovej vzemanje žetone iz trojke
        trojka =  ciljnoPolje.delTrojke()
        if trojka is not None:
            # klinjeni žeton je del trojke, poglej če so vsi nasprotnikovi žetoni del trojk
            znaneTrojke = set(trojka) 
            for polje in self.polje:
                if polje.zeton == nasprotnik and polje not in znaneTrojke:
                    trojka = polje.delTrojke()
                    if trojka is None: # našli smo žeton, ki ni del trojek
                        return False
                    else:
                        znaneTrojke = znaneTrojke.union(trojka)
        # žeton ni del trojke oz so očitno res vsi žetoni del trojk, zato dovoli vzeti žeton
        return True
        

    def konecPoteze(self):
        self.naPotezi = 1 + self.naPotezi % 2
        self.opisStanja = "Igralec %d na potezi ..." % (self.naPotezi,)

    def klikDol(self, event):
        self.miskinGumbDol = True
        # shranimo polje, na katerega smo kliknili
        self.izvornoPolje = self.poljeNaPoziciji(event.pos)
        # če premikamo žetone, nastavi še kateri žeton premikamo
        if self.stadijIgre == 'POLAGANJE/PREMIKANJE' and self.igralec[self.naPotezi-1].zetonovProstih <= 0:
            if self.izvornoPolje and self.izvornoPolje.zeton == self.igralec[self.naPotezi-1]:
                self.lebdeciZeton.zeton = self.igralec[self.naPotezi-1]
                self.izvornoPolje.izprazni()

    def klikGor(self, event):
        # v kolikor prej nismo nikamor kliknili, ignoriraj dogodek
        if self.izvornoPolje is None:
            return
        
        if self.stadijIgre == 'POLAGANJE/PREMIKANJE':
            if self.igralec[self.naPotezi-1].zetonovProstih > 0: # POLAGANJE
                # če smo še vedno nad istim, praznim poljem:
                if self.izvornoPolje.znotraj(event.pos) and self.izvornoPolje.prosto():
                    self.izvornoPolje.zeton = self.igralec[self.naPotezi-1]
                    self.igralec[self.naPotezi-1].zetonNaDesko()
                    # preveri če smo dosegli tri v vrsto
                    if self.izvornoPolje.delTrojke():
                        self.stadijIgre = 'VZEMANJE'
                        self.opisStanja = "Igralec %d je sestavil tri v vrsto ..." % self.naPotezi
                    else:
                        self.konecPoteze()

            elif self.lebdeciZeton.zeton == self.igralec[self.naPotezi-1]: # PREMIKANJE
                ciljnoPolje = self.poljeNaPoziciji(event.pos)
                if ciljnoPolje is not None and ciljnoPolje.prosto() and ciljnoPolje.sosednjePolje(self.izvornoPolje):
                    ciljnoPolje.zeton = self.lebdeciZeton.zeton
                    self.lebdeciZeton.izprazni()
                    # preveri če smo dosegli tri v vrsto
                    if ciljnoPolje.delTrojke():
                        self.stadijIgre = 'VZEMANJE'
                        self.opisStanja = "Igralec %d je sestavil tri v vrsto ..." % self.naPotezi
                    else:
                        self.konecPoteze()
                else:
                    # vrni žeton na prejšnje mesto
                    self.izvornoPolje.zeton = self.lebdeciZeton.zeton
                    self.lebdeciZeton.izprazni()

        elif self.stadijIgre == 'VZEMANJE':
            nasprotnik = self.igralec[self.naPotezi % 2]
            if self.izvornoPolje.znotraj(event.pos) and self.zetonDovoljenoVzeti(self.izvornoPolje, nasprotnik):
                self.izvornoPolje.izprazni()
                nasprotnik.zetonVzet()
                # poglejmo, če je to zmagovalna poteza
                if nasprotnik.izgubil():
                    self.konecIgre = True
                    self.opisStanja = ("Konec igre, igralec %d je zmagal!" % (self.naPotezi,))
                    self.miskinGumbDol = False
                    return
                # določimo, kako naj se igra nadaljuje
                self.stadijIgre = 'POLAGANJE/PREMIKANJE'
                self.konecPoteze()

        # zaključi
        self.miskinGumbDol = False
        self.izvornoPolje = None

    def status(self):
        return self.opisStanja;
    
    def izrisiDesko(self, platno, debelinaCrt = 3):
        '''Izrise igralno desko
         povrsina => pygame.Surface
         pravokotnik => pygame.Rect -> (levo, zgoraj, širina, višina)'''
        x, y = self.deska.topleft
        sirina, visina = self.deska.size
        pygame.draw.rect(platno,(255,   0, 255), self.deska,2)
        # izrisi kvadrate
        for i in [0, 1, 2]:
            pygame.draw.rect(platno,crna,[x+int(i*sirina/6),y+int(i*visina/6),
                                          int((6-2*i)*sirina/6),int((6-2*i)*visina/6)],debelinaCrt)
        # izrisi povezave med kvadrati
        pygame.draw.line(platno,crna,(x,y+visina//2),(x+2*self.razmak,y+visina//2),debelinaCrt)
        pygame.draw.line(platno,crna,(x+4*sirina//6,y+visina//2),(x+sirina,y+visina//2),debelinaCrt)
        pygame.draw.line(platno,crna,(x+sirina//2,y),(x+sirina//2,y+2*visina//6),debelinaCrt)
        pygame.draw.line(platno,crna,(x+sirina//2,y+int(4*visina/6)),(x+sirina//2,y+visina),debelinaCrt)
        # izrisi zetone
        for polje in self.polje:
            polje.izrisiZeton(platno)
        # izrisi lebdeči žeton
        self.lebdeciZeton.center = pygame.mouse.get_pos()
        self.lebdeciZeton.izrisiZeton(platno)
        # izriši proste žetone za prvega igralca
        self.igralec[0].izrisiProsteZetone(platno, self.polmerPolja)
        self.igralec[1].izrisiProsteZetone(platno, self.polmerPolja)

