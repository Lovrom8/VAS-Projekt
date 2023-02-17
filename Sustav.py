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
        self.btn.bind(on_press = self.callback)

        self.img = AsyncImage(source='ML/images/RandomHuman1.jpg',  nocache=True)

        self.add_widget(self.img)
        self.add_widget(self.btn)

        self.pokrenuto = False

    def promjenaSlikeCallback(self, slikaPutanja):
        print(f"Postavljam sliku {slikaPutanja}")
        self.img.source = slikaPutanja 
        self.img.reload()

    def callback(self, event):
        aTrosilo = AgentHVAC(adresaTrosila, "jabber", adresaKontrolera)
        aKontroler = AgentKontroler(adresaKontrolera, "jabber", [adresaTrosila], adresaPrisutnosti)
        aPrisutnost = AgentPrisutnost(adresaPrisutnosti, "jabber", adresaKontrolera, self.promjenaSlikeCallback)

        if self.pokrenuto:
            print("Gasim agente")

            aTrosilo.stop()
            aKontroler.stop()
            aPrisutnost.stop()
            spade.quit_spade()

            self.pokrenuto = False
            self.btn.text = 'Sustav ugašen'
        else:  
            print("Pokrecem agente")

            f = aTrosilo.start()
            f3 = aPrisutnost.start()
            f2 = aKontroler.start()

            print(f.result())
            print(f2.result())
            print(f3.result())

            self.pokrenuto = True
            self.btn.text = 'Sustav pokrenut'

class Aplikacija(App):
    def build(self):
        return GlavniZaslon()

if __name__ == '__main__':
    Aplikacija().run()
