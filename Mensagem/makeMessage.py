import boto3
import json
import threading
import time

# Configuração do SQS
sqs = boto3.client('sqs', region_name='us-east-1')  # Altere para sua região
CHAT_QUEUE_URL = 'URL_DA_FILA_CHAT_QUEUE'  # Substitua pelo URL da sua fila
RESPONSE_QUEUE_URL = 'URL_DA_FILA_RESPONSE_QUEUE'  # Substitua pelo URL da sua fila

# Dicionário para armazenar salas de chat e usuários
salas = {}

def criar_sala(nome_sala):
    """Cria uma nova sala de chat."""
    if nome_sala not in salas:
        salas[nome_sala] = []
        print(f"Sala '{nome_sala}' criada com sucesso!")
    else:
        print(f"Sala '{nome_sala}' já existe.")

def entrar_sala(nome_sala, usuario):
    """Adiciona um usuário a uma sala de chat."""
    if nome_sala in salas:
        salas[nome_sala].append(usuario)
        print(f"'{usuario}' entrou na sala '{nome_sala}'.")
    else:
        print(f"Sala '{nome_sala}' não existe.")

def enviar_mensagem(nome_sala, usuario, mensagem):
    """Envia uma mensagem para a fila SQS."""
    payload = {
        'sala': nome_sala,
        'usuario': usuario,
        'mensagem': mensagem
    }
    sqs.send_message(
        QueueUrl=CHAT_QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
    print(f"Mensagem enviada por '{usuario}' na sala '{nome_sala}'.")

def receber_mensagens():
    """Recebe mensagens da fila SQS em um loop infinito."""
    while True:
        response = sqs.receive_message(
            QueueUrl=CHAT_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )
        if 'Messages' in response:
            for message in response['Messages']:
                payload = json.loads(message['Body'])
                sala = payload['sala']
                usuario = payload['usuario']
                mensagem = payload['mensagem']
                print(f"[{sala}] {usuario}: {mensagem}")
                # Deleta a mensagem da fila após processar
                sqs.delete_message(
                    QueueUrl=CHAT_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
        time.sleep(1)

# Inicia uma thread para receber mensagens
threading.Thread(target=receber_mensagens, daemon=True).start()

# Exemplo de uso
if __name__ == "__main__":
    criar_sala("Geral")
    entrar_sala("Geral", "Alice")
    enviar_mensagem("Geral", "Alice", "Olá, pessoal!")