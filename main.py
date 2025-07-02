import time
import requests
from mcstatus import JavaServer

# === CONFIGURAÇÕES ===
ENDERECO_SERVIDOR = "147.185.221.27"  # Coloque o IP ou domínio aqui
PORTA = 25901  # Porta do servidor Minecraft
INTERVALO = 10  # Tempo entre verificações (em segundos)
WEBHOOK_URL = "https://l.webhook.party/hook/SthM1AJXSjBRJncV3lxlsCmlOlTyvJHaP5y17G3kx12SUaxzAUPe3N2rbOhoZgk86FsU9r14PGsk%2FPuVSB4gayTVc5ZOUM%2BzCD9tG9ImCWzs4K5PaX1yG%2BYpx%2Fs9J0PZ8%2BNE3%2BDQKqjuOJcfxZ0%2BhtOXQmiYppk4J0r3qN4a5n1nvBSbq42%2BY0xCqM2riPhVKRX9TRKHBObzQbmg%2FpCKVOqjMYhPvItFrPNDtjogneDac7k1pT8M89NwwICOH1gHe0RkKbgNBwKKDVgh5hln2NAYEPk60WN%2FhDrudseVpJoX%2BK5DuHXguvGVligJ89gaUt%2FbS45AUoqoDas%2B2nUpAs2d%2FqGl%2BM7Y9hczaU4RvKXVGC8HdUV%2BQMVUqRctxTo1%2BxZRAOfDNmg%3D/iftWpb0BVy5yqvkR"  # Substitua pelo seu webhook

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
