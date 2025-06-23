import time
import requests
from mcstatus import JavaServer

# === CONFIGURAÇÕES ===
ENDERECO_SERVIDOR = "147.185.221.27"  # Coloque o IP ou domínio aqui
PORTA = 25901  # Porta do servidor Minecraft
INTERVALO = 10  # Tempo entre verificações (em segundos)
WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1386754525930721390/HaJv_0yeTe7iOGbWUkitKi_sUAtpoNJFGK7rQK3bdErlUlmQp7hHlmbfwtRe93fQbJPV"  # Substitua pelo seu webhook

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
