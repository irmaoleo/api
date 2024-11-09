import os
import stripe
import json
from fastapi import APIRouter, HTTPException, Header, Request
from .services.emails import send_email
from .auth import create_user, CreatedUserRequest

import json
import random
import string

def password_generator():
    caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    senha = ''.join(random.choice(caracteres) for _ in range(6))  # Gera uma senha de 6 caracteres
    return senha

async def extract_transaction_details(byte_data: bytes) -> dict:
    # Converte os bytes para uma string JSON e, em seguida, para um dicionário
    json_string = byte_data.decode("utf-8")
    data = json.loads(json_string)
    
    # Extração das informações necessárias
    try:
        # Navega pelo dicionário para extrair os campos desejados
        customer_email = data["data"]["object"].get("customer_email")
        customer_name = data["data"]["object"].get("customer_name")
        customer_phone = data["data"]["object"].get("customer_phone")
        status = data["data"]["object"].get("status")

        # Verifica o status da transação
        transaction_status = True if status == "paid" else False
        
        # Retorna o dicionário com as informações extraídas
        
        password = password_generator()
        
        create_user_payload = CreatedUserRequest(email=customer_email, password=password)
        
        if transaction_status == True:
            await create_user(create_user_payload)
            
            send_email({
            "email": customer_email,
            "password": password,
            "full_name": customer_name}, "liberando acesso")
        else:
             send_email({
            "email": customer_email,
            "full_name": customer_name}, "compra não efetuada")
        
        return {
            "email": customer_email,
            "nome_completo": customer_name,
            "telefone": customer_phone,
            "status": transaction_status
        }
    except KeyError as e:
        print(f"Erro ao extrair dados: chave {e} não encontrada.")
        # Retorna um dicionário indicando erro caso alguma chave não seja encontrada
        return {
            "email": None,
            "nome_completo": None,
            "telefone": None,
            "status": "Erro ao processar transação"
        }








router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    # result = extract_event_details(payload)
    
    print('payload')
    payload_dict = await extract_transaction_details(payload)
    
    print(payload_dict)
        
        