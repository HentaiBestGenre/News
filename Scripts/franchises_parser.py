from Services import IGDB
import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

client_id = 'k94eqeuau4fkat8yih6utw06h8b5lf'
secret_key = 'ruxijny32hunyfpa8m8vfoskm0ogk6'
access_token = "ot866i6dteo91c3teidmagbkgymk4r"


client = IGDB(client_id, secret_key, access_token)
print(client)

f1 = client.get_franchises(0)
f1 = json.loads(f1)
f2 = client.get_franchises(500)
f2 = json.loads(f2)
f3 = client.get_franchises(1000)
f3 = json.loads(f3)
f4 = client.get_franchises(1500)
f4 = json.loads(f4)
f = f1 + f2 + f3 + f4