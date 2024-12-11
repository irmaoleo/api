from fastapi import APIRouter, Request

from ..database import supabase

webhook = APIRouter(prefix="/webhook", tags=["webhook"])

@webhook.post("/framer/{owner}/{source}")
async def framer_webhook(request: Request, owner: str, source: str):
    try:
        body = await request.json()
        
        response = (
        supabase.table("leads")
        .insert({"level": 1, "source": source, "owner": owner, "data": body})
        .execute()
        )
        
        # foillow up email
        

        return {"message": "JSON recebido com sucesso", "data": body}
    except Exception as e:
        return {"error": "Não foi possível processar o JSON", "details": str(e)}