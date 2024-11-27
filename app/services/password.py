import random
import string


def password_generator():
    caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    senha = ''.join(random.choice(caracteres) for _ in range(6))  # Gera uma senha de 6 caracteres
    return senha