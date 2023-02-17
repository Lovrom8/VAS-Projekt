from spade.message import Message
import json

class PostaviTemperaturu(Message):
    def __init__(self, od, odrediste, zeljenaTemperatura):
        super().__init__()
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")  
        self.sender = od   
        self.to = odrediste
        self.body = json.dumps({'naredba': 'PostaviTemperaturu', 'zeljenaTemperatura':zeljenaTemperatura})

class DajTemperaturu(Message):
     def __init__(self, od, odrediste):
        super().__init__()
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr") 
        self.sender = od    
        self.to = odrediste
        self.body = json.dumps({'naredba': 'DajTemperaturu'})

class TrenutnaTemperatura(Message):
    def __init__(self, od, odrediste, trenutnaTemperatura):
        super().__init__()
        self.set_metadata("performative", "inform")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")     
        self.sender = od
        self.to = odrediste
        self.body = json.dumps({'naredba': 'TrenutnaTemperatura', 'trenutnaTemperatura':trenutnaTemperatura})
        
class DajStanjePrisustva(Message):
     def __init__(self, od, odrediste):
        super().__init__()
        self.set_metadata("performative", "request")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")  
        self.sender = od   
        self.to = odrediste
        self.body = json.dumps({'naredba': 'DajPrisustvo'})
        
class TrenutnoStanjePrisustva(Message):
     def __init__(self, od, odrediste, prisutan):
        super().__init__()
        self.set_metadata("performative", "inform")
        self.set_metadata("ontology", "smart-building-lp")  
        self.set_metadata("language", "hr")    
        self.sender = od 
        self.to = odrediste
        self.body = json.dumps({'naredba': 'StanjePrisustva', 'prisutan': prisutan})
        