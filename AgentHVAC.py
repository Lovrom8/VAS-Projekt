import spade 
import time
from datetime import timedelta, datetime
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, PeriodicBehaviour, State
from spade.message import Message
from spade.template import Template
import random

STANJE_CEKANJA = "STATE_CEKANJA"
STANJE_OBRADE = "STANJE_OBRADE"
STANJE_GRIJANJA = "STANJE_GRIJANJA"
STANJE_MJERENJA = "STANJE_MJERENJA"
STANJE_IZVJESCIVANJA = "STANJE_IZVJESCIVANJA"

TrenutnaTemp = 15
CiljnaTemp = 25
DeltaTemp = 1

class AgentHVAC(Agent):
    def __init__(self, jid, password, adresaKontrolera):
        super().__init__(jid, password)
        self.adresaKontrolera = adresaKontrolera

    class HVACFSMPonasanje(FSMBehaviour):
        async def on_start(self):
            print(f"HVAC zapocinje u stanju: {self.current_state}")
            self.posljednjaPoruka = ""

    class StanjeCekanjaPoruke(State):
        async def run(self):
            print("HVAC: u stanju cekanja poruke")
            msg = await self.receive(timeout=60)

            self.agent.posljednjaPoruka = msg.body
            self.set_next_state(STANJE_OBRADE)
   
    class StanjeObradePoruke(State):
        async def run(self):
            print(f"HVAC: obradujem poruku {self.agent.posljednjaPoruka}")

            dijelovi = self.agent.posljednjaPoruka.split()
            naredba = dijelovi[0]
            naziv = dijelovi[1]
            self.agent.posljednjiNaziv = naziv

            if "temperatura" in naredba:
                self.set_next_state(STANJE_GRIJANJA)
            elif "mjeri" in naredba:
                self.set_next_state(STANJE_MJERENJA)

    class StanjeMjerenja(State):
        async def run(self):
            sleep(1)
            if ("temperatura" in self.posljednjaPoruka):
                if (TrenutnaTemp < CiljnaTemp):
                    self.set_next_state(STANJE_GRIJANJA)
                else:
                    self.set_next_state(STANJE_CEKANJA)  
            elif ("mjeri" in self.posljednjaPoruka):
                self.set_next_state(STANJE_IZVJESCIVANJA)

            return
    
    class StanjeIzvjescivanja(State):
        async def run(self):
            self.posaljiNaredbu(f"izvjestaj {TrenutnaTemp}")
            self.set_next_state(STANJE_OBRADE)
            return
    
    class StanjeGrijanja(State):
        async def run(self):
            TrenutnaTemp += DeltaTemp
            self.set_next_state(STANJE_MJERENJA)
            return

    async def setup(self):
        print("Inicijaliziram HVAC")
        self.posljednjaPoruka = ""
        self.posljednjiNaziv = ""

        fsm = self.HVACFSMPonasanje()
        self.dodajStanja(fsm)
        self.dodajTranzicije(fsm)

        template = Template()
        template.set_metadata("performative", "request")

        self.add_behaviour(fsm, template)

    async def posaljiNaredbu(self, naziv, naredba):
            sadrzaj = f"{naredba} {naziv}"
                
            print(f"Okruzje: Saljem narudzbu {sadrzaj}")
            msg = Message(to="lovrom8@c99x.io")
            msg.set_metadata("performative", "request")
            msg.body = sadrzaj
            await self.send(msg)

    def dodajStanja(self, fsm):
        fsm.add_state(name=STANJE_CEKANJA, state=self.StanjeCekanjaPoruke(), initial=True)
        fsm.add_state(name=STANJE_OBRADE, state=self.StanjeObradePoruke())
        fsm.add_state(name=STANJE_GRIJANJA, state=self.StanjeGrijanja())
        fsm.add_state(name=STANJE_IZVJESCIVANJA, state=self.StanjeIzvjescivanja())
        fsm.add_state(name=STANJE_MJERENJA, state=self.StanjeMjerenja())
        return

    def dodajTranzicije(self, fsm):
        fsm.add_transition(source=STANJE_CEKANJA, dest=STANJE_OBRADE)
        fsm.add_transition(source=STANJE_OBRADE, dest=STANJE_GRIJANJA)
        fsm.add_transition(source=STANJE_OBRADE, dest=STANJE_MJERENJA)
        fsm.add_transition(source=STANJE_GRIJANJA, dest=STANJE_MJERENJA)
        fsm.add_transition(source=STANJE_MJERENJA, dest=STANJE_IZVJESCIVANJA)
        fsm.add_transition(source=STANJE_IZVJESCIVANJA, dest=STANJE_CEKANJA)
        return