import time
from datetime import timedelta, datetime
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import random
import json
from Naredbe import * 

class AgentKontroler(Agent):
    def __init__(self, jid, password, trosila, adresaPrisutnosti):
        super().__init__(jid, password)
        self.trosilo = trosila[0]
        self.kontrolerPrisutnosti = adresaPrisutnosti
    
    class KontrolerPonasanje(PeriodicBehaviour):
        async def on_start(self):
            print("Kontroler zapocinje s radom")

        async def obradiStanjePrisutnosti(self, sadrzaj):
            print("Agent kontroler - obrađujem stanje prisustva")
            sadrzaj = json.loads(sadrzaj)

            print(sadrzaj)

            if sadrzaj['prisutan']:
                msg = PostaviTemperaturu("Kontroler", self.agent.trosilo, 10)
                await self.send(msg)
            
            return
        
        async def obradiIzvjestajOTemperaturi(self, sadrzaj):
            return

        async def obradiPoruku(self, msg):
            naredba = msg.body

            if "StanjePrisustva" in naredba:
                await self.obradiStanjePrisutnosti(msg.body)
            elif "DajTemperaturu" in naredba:
                await self.obradiIzvjestajOTemperaturi(msg.body)

        async def run(self):
            msg = DajStanjePrisustva("Kontroler", self.agent.kontrolerPrisutnosti)
            await self.send(msg)

            msg = await self.receive(timeout=0)

            if msg is not None:
                await self.obradiPoruku(msg)
    
    async def setup(self):
        print("Inicijaliziram Kontroler")

        ag = self.KontrolerPonasanje(period=5)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(ag, template)