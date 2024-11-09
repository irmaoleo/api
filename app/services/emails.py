import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .email_templates.index import render_succed_email

def send_email(dados_usuario, tipo_email):
    # Configurações do email remetente
    email_remetente = "firetestnaoresponda@gmail.com"
    senha = "kncq nfpn mzpm iuom"
    
    # Destinatário
    email_destinatario = dados_usuario["email"]
    password_destinatario = dados_usuario["password"]
    nome_destinatario = dados_usuario["full_name"]
    
    # Assunto e corpo do email com base no tipo de email
    if tipo_email == "liberando acesso":
        assunto = "👨‍💻Acesso ao APP Firetest Liberado"
        corpo_email = render_succed_email({
            "email": email_destinatario,
            "password": password_destinatario
        })
    elif tipo_email == "compra não efetuada":
        assunto = "Compra Não Efetuada"
        corpo_email = f"Olá, {nome_destinatario}.\n\nNão foi possível efetuar a compra. Por favor, verifique seus dados e tente novamente ou entre em contato com nosso suporte."
    else:
        raise ValueError("Tipo de email inválido")

    # Configuração da mensagem
    mensagem = MIMEMultipart()
    mensagem["From"] = email_remetente
    mensagem["To"] = email_destinatario
    mensagem["Subject"] = assunto
    mensagem.attach(MIMEText(corpo_email, "html"))

    # Enviando o email
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(email_remetente, senha)
        servidor.sendmail(email_remetente, email_destinatario, mensagem.as_string())
        print(f"Email enviado com sucesso para {nome_destinatario}!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    finally:
        servidor.quit()
