import time
from datetime import timedelta, datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from os import listdir
import random
from keras.models import load_model 
from PIL import Image, ImageOps
import numpy as np
from Naredbe import *

class AgentPrisutnost(Agent):
    def __init__(self, jid, password, adresaKontrolera, promjenaSlikeCallback):
        super().__init__(jid, password)
        self.adresaKontrolera = adresaKontrolera
        self.promjenaSlikeCallback = promjenaSlikeCallback
        self.model = load_model("./ML/model.h5", compile=False)

    class PrisutnostPonasanje(CyclicBehaviour):
        async def on_start(self):
            print("Agent za prisutnost zapocinje s radom")

        def odaberiSlucajno(self):
            slikaPath = random.choice(listdir("./ML/images"))
            return f'./ML/images/{slikaPath}'

        async def provjeri(self, slikaPutanja):
            naziviKlasa = ["RandomHuman", "NotHuman"]

            velicina = (224, 224)
            image = Image.open(slikaPutanja).convert("RGB")
            image = ImageOps.fit(image, velicina, Image.LANCZOS)

            image_array = np.asarray(image)

            normaliziranaSlika = (image_array.astype(np.float32) / 127.5) - 1

            podaci = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            podaci[0] = normaliziranaSlika

            prediction = self.agent.model.predict(podaci)
            index = np.argmax(prediction)
            nazivKlase = naziviKlasa[index]
            confidence_score = prediction[0][index]

            print(f"Prisustvo: slika - {slikaPutanja}")
            print("Klasa:", nazivKlase, end="")
            print("Vjerojatnost:", confidence_score)

            self.agent.promjenaSlikeCallback(slikaPutanja)

            return nazivKlase
        
        async def obradiPoruku(self, msg):
            if 'DajPrisustvo' in msg.body:
                klasa = await self.provjeri(self.odaberiSlucajno())
                prisutan = "RandomHuman" in klasa
                
                poruka = TrenutnoStanjePrisustva("AgentPrisustvo", self.agent.adresaKontrolera, prisutan)
                await self.send(poruka)

        async def run(self):
            msg = await self.receive(timeout=0)

            if msg is not None:
               await self.obradiPoruku(msg)
    
    async def setup(self):
        self.prisutnostPonasanje = self.PrisutnostPonasanje()
        self.narudzbe = []

        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(self.prisutnostPonasanje, template)