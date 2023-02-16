from AgentHVAC import *
from AgentKontroler import *
from AgentPrisutnost import *

adresaTrosila = "lovrom8@c99x.io"
adresaKontrolera = "lovrom8Okruzenje@c99x.io" 
adresaPrisutnosti = "lovrop@c99x.io"

if __name__ == '__main__':
    aTrosilo = AgentHVAC(adresaTrosila, "jabber", adresaKontrolera)
    aKontroler = AgentKontroler(adresaKontrolera, "jabber", [adresaTrosila])
    #aPrisutnost = AgentPrisutnost(adresaPrisutnosti, "jabber", adresaKontrolera)
    f = aTrosilo.start()
    f2 = aKontroler.start()
    #f3 = aPrisutnost.start()

    print(f.result())
    print(f2.result())
    #print(f3.result())

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nZaustavljam agente...")
    
    aTrosilo.stop()
    aKontroler.stop()
    aPrisutnost.stop()
    spade.quit_spade()