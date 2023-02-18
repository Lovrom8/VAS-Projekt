import spade

from AgentHVAC import *
from AgentKontroler import *
from AgentPrisutnost import *

import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage

adresaTrosila = "lovrom8@c99x.io"
adresaKontrolera = "lovrom8Okruzenje@c99x.io" 
adresaPrisutnosti = "lovrop@c99x.io"

class GlavniZaslon(GridLayout):
    def __init__(self, **kwargs):
        super(GlavniZaslon, self).__init__(**kwargs)
        self.cols = 2
        self.btn = Button(text ="Pokreni sustav", font_size ="20sp")
        self.btn.bind(on_press = self.gumbKlikCallback)

        self.img = AsyncImage(source='ML/images/RandomHuman1.jpg',  nocache=True)
        self.lblTemperatura = Label(text = "Temperatura (C)", font_size ="20sp")
        self.lblGrijanje = Label(text = "Grijanje", font_size ="20sp")
        
        self.lblTrenutnaTemperatura = Label(text = "Čeka se mjerenje", font_size ="20sp")
        self.lblTrenutnoGrijanje = Label(text = "Isključeno", font_size ="20sp", color=(1,0,0,0.5))
        
        self.add_widget(self.img)
        self.add_widget(self.btn)
        self.add_widget(self.lblTemperatura)
        self.add_widget(self.lblTrenutnaTemperatura)
        self.add_widget(self.lblGrijanje)
        self.add_widget(self.lblTrenutnoGrijanje)
        
        self.pokrenuto = False

    def promjenaSlikeCallback(self, slikaPutanja):
        print(f"App: postavljam sliku {slikaPutanja}")
        self.img.source = slikaPutanja 
        self.img.reload()
        
    def promjenaStanjaCallback(self, prisutnost, temperatura):
        print(f'App: promjena stanja {prisutnost} {temperatura}')
        
        if prisutnost:
            self.lblTrenutnoGrijanje.text = 'Uključeno'
            self.lblTrenutnoGrijanje.color = (0,0.9,0,0.5)
        else:
            self.lblTrenutnoGrijanje.text = 'Isključeno'
            self.lblTrenutnoGrijanje.color = (1,0,0,0.5)

        if temperatura is not None:
            self.lblTrenutnaTemperatura.text = str(temperatura)    
        return

    def gumbKlikCallback(self, event):
        aTrosilo = AgentHVAC(adresaTrosila, "jabber", adresaKontrolera)
        aKontroler = AgentKontroler(adresaKontrolera, "jabber", [adresaTrosila], adresaPrisutnosti, self.promjenaStanjaCallback)
        aPrisutnost = AgentPrisutnost(adresaPrisutnosti, "jabber", adresaKontrolera, self.promjenaSlikeCallback)

        if self.pokrenuto:
            print("App: gasim agente")

            aTrosilo.stop()
            aKontroler.stop()
            aPrisutnost.stop()
            spade.quit_spade()

            self.pokrenuto = False
            self.btn.text = 'Sustav ugašen'
        else:  
            print("App: pokrecem agente")

            f = aTrosilo.start()
            f3 = aPrisutnost.start()
            f2 = aKontroler.start()

            #print(f.result())
            #print(f2.result())
            #print(f3.result())

            self.pokrenuto = True
            self.btn.text = 'Sustav pokrenut'

class Aplikacija(App):
    def build(self):
        self.title = 'Skoro pametan sustav za grijanje'
        return GlavniZaslon()

if __name__ == '__main__':
    Aplikacija().run()
