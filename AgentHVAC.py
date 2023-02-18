from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.template import Template
from Naredbe import *

STANJE_CEKANJA = "STATE_CEKANJA"
STANJE_OBRADE = "STANJE_OBRADE"
STANJE_GRIJANJA = "STANJE_GRIJANJA"
STANJE_MJERENJA = "STANJE_MJERENJA"
STANJE_IZVJESCIVANJA = "STANJE_IZVJESCIVANJA"

class AgentHVAC(Agent):
    def __init__(self, jid, password, adresaKontrolera):
        super().__init__(jid, password)
        self.kontroler = adresaKontrolera
        self.TrenutnaTemp = 15
        self.CiljnaTemp = 25
        self.DeltaTemp = 1
        self.TemperaturaVani = 10

    class HVACFSMPonasanje(FSMBehaviour):
        async def on_start(self):
            print(f"HVAC zapocinje u stanju: {self.current_state}")
            self.posljednjaPoruka = ""

    class StanjeCekanjaPoruke(State):
        async def run(self):
            print("HVAC: u stanju cekanja poruke")
            msg = await self.receive(timeout=30)

            if (msg is not None):
                self.agent.posljednjaPoruka = msg.body
                self.set_next_state(STANJE_OBRADE)
            else:
                self.set_next_state(STANJE_CEKANJA)
                if (self.agent.TrenutnaTemp > self.agent.TemperaturaVani):
                    self.agent.TrenutnaTemp -= 1
   
    class StanjeObradePoruke(State):
        async def run(self):
            print(f"HVAC: obradujem poruku {self.agent.posljednjaPoruka}")

            sadrzaj = json.loads(self.agent.posljednjaPoruka)
            if "PostaviTemperaturu" in sadrzaj['naredba']:
                self.agent.CiljnaTemp = sadrzaj['zeljenaTemperatura']
                self.set_next_state(STANJE_GRIJANJA)
            elif "DajTemperaturu" in sadrzaj['naredba']:
                self.set_next_state(STANJE_MJERENJA)

    class StanjeMjerenja(State):
        async def run(self):
            print(f"HVAC: u stanju STANJE_MJERENJA")
            
            if ("PostaviTemperaturu" in self.agent.posljednjaPoruka):
                if (self.agent.TrenutnaTemp < self.agent.CiljnaTemp):
                    self.set_next_state(STANJE_GRIJANJA)
                else:
                    self.set_next_state(STANJE_CEKANJA)  
            elif ("DajTemperaturu" in self.agent.posljednjaPoruka):
                self.set_next_state(STANJE_IZVJESCIVANJA)

            return
    
    class StanjeIzvjescivanja(State):
        async def run(self):
            print(f"HVAC: u stanju STANJE_IZVJESCIVANJA")
            
            msg = TrenutnaTemperatura("HVAC 1", self.agent.kontroler, self.agent.TrenutnaTemp)
            await self.send(msg)
            self.set_next_state(STANJE_CEKANJA)
            return
    
    class StanjeGrijanja(State):
        async def run(self):
            print(f"HVAC: u stanju STANJE_GRIJANJA")
            
            self.agent.TrenutnaTemp += self.agent.DeltaTemp
            self.set_next_state(STANJE_MJERENJA)
            return

    async def setup(self):
        print("HVAC: Inicijaliziram")
        self.posljednjaPoruka = ""

        fsm = self.HVACFSMPonasanje()
        self.dodajStanja(fsm)
        self.dodajTranzicije(fsm)

        template = Template()
        template.set_metadata("performative", "request")

        self.add_behaviour(fsm, template)

    def dodajStanja(self, fsm):
        fsm.add_state(name=STANJE_CEKANJA, state=self.StanjeCekanjaPoruke(), initial=True)
        fsm.add_state(name=STANJE_OBRADE, state=self.StanjeObradePoruke())
        fsm.add_state(name=STANJE_GRIJANJA, state=self.StanjeGrijanja())
        fsm.add_state(name=STANJE_IZVJESCIVANJA, state=self.StanjeIzvjescivanja())
        fsm.add_state(name=STANJE_MJERENJA, state=self.StanjeMjerenja())
        return

    def dodajTranzicije(self, fsm):
        fsm.add_transition(source=STANJE_CEKANJA, dest=STANJE_CEKANJA)
        fsm.add_transition(source=STANJE_CEKANJA, dest=STANJE_OBRADE)
        fsm.add_transition(source=STANJE_OBRADE, dest=STANJE_GRIJANJA)
        fsm.add_transition(source=STANJE_OBRADE, dest=STANJE_MJERENJA)
        fsm.add_transition(source=STANJE_GRIJANJA, dest=STANJE_MJERENJA)
        fsm.add_transition(source=STANJE_MJERENJA, dest=STANJE_GRIJANJA)
        fsm.add_transition(source=STANJE_MJERENJA, dest=STANJE_IZVJESCIVANJA)
        fsm.add_transition(source=STANJE_MJERENJA, dest=STANJE_CEKANJA)
        fsm.add_transition(source=STANJE_IZVJESCIVANJA, dest=STANJE_CEKANJA)
        return