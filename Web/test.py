import requests
from hashlib import md5
from tqdm import trange


def crack_password(pass_start, id):
    for i in trange(256**3):
        for j in range(0, 256, 16):
            str = f"password-<function token_hex at {id}{i:x}{j:x}>"
            hash = md5(str.encode()).hexdigest()
            if hash.startswith(pass_start):
                print(f"Potential password: {hash}")
                
id = 135598316332944                
id = hex(int(id))[:6]                           
crack_password("1797c2", id)
