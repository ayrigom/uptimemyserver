import time
import requests
from mcstatus import JavaServer

# === CONFIGURAÇÕES ===
ENDERECO_SERVIDOR = "147.185.221.27"  # Coloque o IP ou domínio aqui
PORTA = 25901  # Porta do servidor Minecraft
INTERVALO = 10  # Tempo entre verificações (em segundos)
WEBHOOK_URL = "https://l.webhook.party/hook/pVV5SDBqnixgp7auP4VWiMA46grZwbhJWv7C5ZyWe6B4qVqC8nLTiDB5me6d6lR5eUUzM6L3iOnJbYGrNcWMMg3L60bjh1u2BWM3qkg49pHb41YQNgBvMTNzPPIB1ROUx8WZBKltzjZkttPVCmMYvNPpB6hEqLSRnafeLePQN0jClOqla35nmOqe4E3vpPIeakE6SKN2a5bWhNpShzYeCYCT0eTadZ%2F%2FHUc%2ByXp3K2rUsyFsejRRAsGA30jE0HWO82lkS5rLJj1Ga%2FisLRn7vK4R90JkiEKysNgSGQYgKaxdm7UMsfQ2lsxEF5wbh0yD7LCVsrfaRQkYmrOr0jWNZMSmA7NqOw4U7j1aiH%2FsfjDnbmb930gfFFgw1MI12HaDUnQgzEcV0H8%3D/nrAs0vJMKf%2Fcrn1n"  # Substitua pelo seu webhook

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
