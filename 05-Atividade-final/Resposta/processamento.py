import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("TABLE_NAME", "FeedbacksReclamacoes"))
sns = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]


def inserir_feedback(id_cliente, descricao, categoria, data_hora):
    return table.put_item(
        Item={
            "id_cliente": id_cliente,
            "descricao": descricao,
            "categoria": categoria,
            "data_hora": data_hora,
        }
    )


def notificar_atendimento(feedback):
    assunto = f"Novo(a) {feedback['categoria']} - cliente {feedback['id_cliente']}"
    mensagem = (
        f"Cliente: {feedback['id_cliente']}\n"
        f"Categoria: {feedback['categoria']}\n"
        f"Data/hora: {feedback['data_hora']}\n"
        f"Descricao: {feedback['descricao']}"
    )
    sns.publish(TopicArn=TOPIC_ARN, Subject=assunto[:100], Message=mensagem)


def handler(event, context):
    for record in event["Records"]:
        feedback = json.loads(record["body"])

        inserir_feedback(
            feedback["id_cliente"],
            feedback["descricao"],
            feedback["categoria"],
            feedback["data_hora"],
        )
        notificar_atendimento(feedback)

    return {"processados": len(event["Records"])}
