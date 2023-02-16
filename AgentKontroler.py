import time
from datetime import timedelta, datetime
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, PeriodicBehaviour, State
from spade.message import Message
from spade.template import Template
import random
from Naredbe import * 

class AgentKontroler(Agent):
    def __init__(self, jid, password, trosila):
        super().__init__(jid, password)
        self.trosilo = trosila[0]
    
    class KontrolerPonasanje(PeriodicBehaviour):
        async def on_start(self):
            print("Kontroler zapocinje s radom")

        async def obradiStanjePrisutnosti(self, sadrzaj):
            #if prisutni
            #u budućnosti - if će biti pristuni
            msg = PostaviTemperaturu("Kontroler", self.agent.trosilo, 10)
            await self.send(msg)
            
            return
        
        async def obradiIzvjestajOTemperaturi(self, sadrzaj):
            return

        def obradiPoruku(self, msg):
            naredba = msg.body.naredba

            if "StanjePrisustva" in naredba:
                self.obradiStanjePrisutnosti(msg.body)
            elif "DajTemperaturu" in naredba:
                self.obradiIzvjestajOTemperaturi(msg.body)

        async def run(self):
            print("Kontroler run")
            #msg = PostaviTemperaturu("Kontroler", self.agent.trosilo, 10)
            #await self.send(msg)
            
            msg = await self.receive(timeout=0)

            if msg is not None:
                self.obradiPoruku(msg)
    
    async def setup(self):
        print("Inicijaliziram Kontroler")

        ag = self.KontrolerPonasanje(period=5)
        self.add_behaviour(ag)