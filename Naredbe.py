from spade.message import Message
import json

class PostaviTemperaturu(Message):
    def __init__(self, od, odrediste, zeljenaTemperatura):
        super().__init__()
        self.zeljenaTemperatura = zeljenaTemperatura
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")     
        self.to = odrediste
        self.body = json.dumps({'naredba', 'PostaviTemperaturu'}, {'zeljenaTemperatura':zeljenaTemperatura})

class DajTemperaturu(Message):
     def __init__(self, od, odrediste, zeljenaTemperatura):
        super().__init__()
        self.zeljenaTemperatura = zeljenaTemperatura
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")     
        self.to = odrediste
        self.body = json.dumps({'naredba', 'DajTemperaturu'})
        
class DajStanjePrisustva(Message):
     def __init__(self, od, odrediste, zeljenaTemperatura):
        super().__init__()
        self.zeljenaTemperatura = zeljenaTemperatura
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")     
        self.to = odrediste
        self.body = json.dumps({'naredba', 'DajPrisustvo'})
        
class TrenutnoStanjePrisustva(Message):
     def __init__(self, od, odrediste, zeljenaTemperatura):
        super().__init__()
        self.zeljenaTemperatura = zeljenaTemperatura
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")     
        self.to = odrediste
        self.body = json.dumps({'naredba', 'StanjePrisustva'})
        