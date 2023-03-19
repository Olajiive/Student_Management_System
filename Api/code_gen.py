import random

def code_generator(prefix: str):
    unique_code = random.randint(10000, 90000)
    unique_code = str(unique_code)
    
    num = prefix + unique_code
    return num
    