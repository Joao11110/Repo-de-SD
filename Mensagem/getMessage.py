import boto3
import json
import time

# Configuração do SQS
sqs = boto3.client('sqs', region_name='us-east-1')  # Altere para sua região
CHAT_QUEUE_URL = 'URL_DA_FILA_CHAT_QUEUE'  # Substitua pelo URL da sua fila

def consumir_mensagens():
    """Consome mensagens da fila SQS em um loop infinito."""
    print("Iniciando consumidor de mensagens...")
    while True:
        try:
            # Recebe mensagens da fila
            response = sqs.receive_message(
                QueueUrl=CHAT_QUEUE_URL,
                MaxNumberOfMessages=10,  # Número máximo de mensagens por requisição
                WaitTimeSeconds=5  # Long polling para reduzir o número de chamadas vazias
            )

            # Verifica se há mensagens na fila
            if 'Messages' in response:
                for message in response['Messages']:
                    # Processa a mensagem
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
            else:
                print("Nenhuma mensagem nova na fila. Aguardando...")

        except Exception as e:
            print(f"Erro ao consumir mensagens: {e}")

        # Espera um pouco antes de verificar novamente
        time.sleep(1)

if __name__ == "__main__":
    consumir_mensagens()