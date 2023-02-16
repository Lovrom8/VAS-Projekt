import time
from datetime import timedelta, datetime
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, PeriodicBehaviour, State
from spade.message import Message
from spade.template import Template
import random
import pandas as pd

class LogPrisutnosti:
    def __init(vrijeme):
        self.vrijeme = time()

class AgentPrisutnost(Agent):
    def __init__(self, jid, password, adresaKontrolera):
        super().__init__(jid, password)
        self.adresaKontrolera = adresaKontrolera
  
    class PrisutnostPonasanje(PeriodicBehaviour):
        def obradiPoruku(self, poruka):
            dijelovi = poruka.body.split()
            naredba = dijelovi[0]
            naziv = dijelovi[1]

        async def posaljiNaredbu(self, naziv, naredba):
            sadrzaj = f"{naredba} {naziv}"
                
            print(f"Agent prisutnosti: Saljem narudzbu {sadrzaj}")
            msg = Message(to=self.agent.adresaKontrolera)
            msg.set_metadata("performative", "request")
            msg.body = sadrzaj
            await self.send(msg)

        async def on_start(self):
            print("Agent za prisutnost zapocinje s radom")
            df = pd.read_csv('prisutnost.csv')

        async def run(self):
            msg = await self.receive(timeout=10)

            if msg is not None:
                self.obradiPoruku(msg)

            
    async def setup(self):
        self.prisutnostPonasanje = self.PrisutnostPonasanje(period=1)
        self.narudzbe = []
        self.add_behaviour(self.prisutnostPonasanje)