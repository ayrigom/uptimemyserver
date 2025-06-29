import time
import requests
from mcstatus import JavaServer

# === CONFIGURAÇÕES ===
ENDERECO_SERVIDOR = "147.185.221.27"  # Coloque o IP ou domínio aqui
PORTA = 25901  # Porta do servidor Minecraft
INTERVALO = 10  # Tempo entre verificações (em segundos)
WEBHOOK_URL = "https://l.webhook.party/hook/yo4i7fwUFNxJjL6SfxNdGSjsWtA4gbxGL%2BVZq524Ujukq6MQwgb%2Fr1g0pm95r9CI%2FyTYR4ZlbjKZ1k0qQ9u5I5R4kboPaPBsAgEsM5V8E5CNLfC3YVEDBtuSfuYJP1ioUTWh8N2rEdxcux%2FMoAXUIET4E7jrVgHLMnzXGgdI7FZV0mJqvfo3qQhqBTV6KPBR%2BufSTB1jyIM8ovFnOjMv3z0X%2BcEdNkRRz7y%2FNZR%2FYQCuez7LA4vb1cllkEbXQmybnJUhq50EOU%2FD8c5PUkt%2FEIlzwDquhJoEL%2FZybg7G2i8dsgPw0UeKyRA8gYiPbmgU68mCHb2i9dWTa%2BYygXH4n08AcUv9KcY1rHpYBtDsdlqCeWMDH64KwWiC2UzzOVV%2B9VbsrBTPIxk%3D/FQjVxYbn%2BxATuqT1"  # Substitua pelo seu webhook

# === VARIÁVEL DE CONTROLE ===
ultimo_status_online = None  # Começa sem saber o status

def enviar_webhook(mensagem):
    payload = {
        "content": mensagem
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Webhook enviado com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar webhook: {e}")

def verificar_status():
    global ultimo_status_online
    servidor = JavaServer.lookup(f"{ENDERECO_SERVIDOR}:{PORTA}")
    try:
        status = servidor.status()
        print(f"Status recebido: {status}")
        
        if ultimo_status_online is not True:
            # Servidor ficou online agora
            motd = ' '.join(map(str, status.motd.parsed)) if status.motd and hasattr(status.motd, 'parsed') else "Servidor sem motd"
            enviar_webhook(f":white_check_mark: Servidor Minecraft **online!**\nMotd: {motd}")
            ultimo_status_online = True
        else:
            print("Servidor já estava online, sem envio de webhook.")

    except Exception as e:
        print(f"Erro ao verificar o status: {e}")
        if ultimo_status_online is not False:
            # Servidor caiu agora
            enviar_webhook(":x: Servidor Minecraft **offline ou indisponível!**")
            ultimo_status_online = False
        else:
            print("Servidor já estava offline, sem envio de webhook.")

# === LOOP PRINCIPAL ===
if __name__ == "__main__":
    print("Monitor de servidor Minecraft iniciado.")
    while True:
        verificar_status()
        time.sleep(INTERVALO)
