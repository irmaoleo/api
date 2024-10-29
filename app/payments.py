# from fastapi import APIRouter, HTTPException, Query
# import mercadopago

# router = APIRouter(prefix="/payments", tags=["payments"])

# # Inicialize o SDK do Mercado Pago
# sdk = mercadopago.SDK(
#     # "TEST-6105177808729772-102510-24a147b585383316aa2feafb4f1e30c5-1001701819"
#     "APP_USR-6105177808729772-102510-710cb7afdbd0237b851354d95ec18dbb-1001701819"
# )


# @router.post("/create_checkout")
# async def create_checkout():
#     # Definindo os planos mensal e anual como opções no checkout
#     preference_data = {
#         "items": [
#             # {
#             #     "title": "Assinatura Mensal - R$27,90",
#             #     "quantity": 1,
#             #     "currency_id": "BRL",
#             #     "unit_price": 27.90,
#             # },
#             # {
#             #     "title": "Assinatura Anual - R$19,90/mês",
#             #     "quantity": 1,
#             #     "currency_id": "BRL",
#             #     "unit_price": 238.80,
#             # },
#             {
#                 "title": "Assinatura 12 Meses - R$27,90/mês",
#                 "quantity": 1,
#                 "currency_id": "BRL",
#                 "unit_price": 1.1,
#             },
#         ],
#         "back_urls": {
#             "success": "https://firetest.com.br",
#             "failure": "https://firetest.com.br",
#             "pending": "https://firetest.com.br",
#         },
#         "notification_url": "https://badb-2804-214-8021-8ed4-bc0d-c988-da77-1044.ngrok-free.app/payments/webhook",
#         "auto_return": "approved",
#     }

#     # Cria a preferência de pagamento
#     preference_response = sdk.preference().create(preference_data)
#     preference = preference_response["response"]

#     # Retorna o link para o checkout
#     return {"checkout_url": preference["init_point"]}


# @router.post("/webhook")
# async def mercadopago_webhook(id: str = Query(...), topic: str = Query(...)):
#     """Webhook do Mercado Pago: Lida com diferentes tópicos de notificação."""
#     # try:
#     #     print(f"Notificação recebida - ID: {id}, Tópico: {topic}")

#     #     # Verifique se a notificação é sobre uma ordem de pagamento
#     #     if topic == "merchant_order":
#     #         # Consulta a ordem de pagamento usando o SDK
#     #         merchant_order = sdk.merchant_order().get(id)
            
#     #         print('merchant_order')
#     #         print(merchant_order)


#     #         # Extrai informações da ordem
#     #         response = merchant_order["response"]
#     #         print('response')
#     #         print(response)
#     #         if response.get("status") == "opened":
#     #             payments = response.get("payments", [])
#     #             for payment in payments:
#     #                 if payment["status"] == "approved":
#     #                     payer = payment.get("payer", {})
#     #                     nome_comprador = (
#     #                         payer.get("first_name", "")
#     #                         + " "
#     #                         + payer.get("last_name", "")
#     #                     )
#     #                     email_comprador = payer.get("email", "")

#     #                     print(
#     #                         f"Pagamento aprovado! Nome: {nome_comprador}, Email: {email_comprador}"
#     #                     )
#     #                     # Aqui você pode liberar o acesso ao cliente no sistema

#     #     return {"status": "ok"}

#     # except Exception as e:
#     #     print(f"Erro: {str(e)}")
#     #     raise HTTPException(status_code=400, detail="Erro ao processar a notificação")
    
#     payer_id = '1361916851'
