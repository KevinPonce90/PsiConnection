let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
import random
num = "0123456789"

gen = f"{let}{num}"
lon = 8
ran = random.sample(gen, lon)
cod = "".join(ran)

codVeriPaci = cod

print("Este es el cod: ",codVeriPaci)
