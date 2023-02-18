import time
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.template import Template
import json
from Naredbe import * 

class AgentKontroler(Agent):
    def __init__(self, jid, password, trosila, adresaPrisutnosti, promjenaStanjaCallback):
        super().__init__(jid, password)
        self.agentTrosila = trosila[0]
        self.agentPrisutnosti = adresaPrisutnosti
        self.brojPerioda = 0
        self.promjenaStanjaCallback = promjenaStanjaCallback
        
    class KontrolerPonasanje(PeriodicBehaviour):
        async def obradiStanjePrisutnosti(self, sadrzaj):
            print("Kontroler: obrađujem stanje prisustva")
            sadrzaj = json.loads(sadrzaj)

            if sadrzaj['prisutan']:
                msg = PostaviTemperaturu("Kontroler", self.agent.agentTrosila, 25)
                await self.send(msg)
            
            self.agent.promjenaStanjaCallback(sadrzaj['prisutan'], None)
            
            return
        
        async def obradiIzvjestajOTemperaturi(self, sadrzaj):
            print("Kontroler: obrađujem izvještaj o temperaturi")
            sadrzaj = json.loads(sadrzaj)

            self.agent.promjenaStanjaCallback(None, sadrzaj['trenutnaTemperatura'])
            
            return

        async def obradiPoruku(self, msg):
            naredba = msg.body

            if "StanjePrisustva" in naredba:
                await self.obradiStanjePrisutnosti(msg.body)
            elif "TrenutnaTemperatura" in naredba:
                await self.obradiIzvjestajOTemperaturi(msg.body)

        async def run(self):
            if self.agent.brojPerioda == 5:
                msg = DajTemperaturu("Kontroler", self.agent.agentTrosila)
                self.agent.brojPerioda = 0
            else:
                msg = DajStanjePrisustva("Kontroler", self.agent.agentPrisutnosti)
                self.agent.brojPerioda += 1
            await self.send(msg)

            msg = await self.receive(timeout=3)

            if msg is not None:
                await self.obradiPoruku(msg)
    
    async def setup(self):
        print("Inicijaliziram Kontroler")

        ag = self.KontrolerPonasanje(period=5)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(ag, template)