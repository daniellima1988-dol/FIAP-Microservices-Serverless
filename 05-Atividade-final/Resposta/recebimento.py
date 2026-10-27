import json
import os

import boto3

sqs = boto3.client("sqs")
QUEUE_URL = os.environ["QUEUE_URL"]


def handler(event, context):
    # O corpo ja chega validado pelo JSON Schema do API Gateway
    body = event.get("body") or "{}"

    response = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=body)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "mensagem": "Feedback recebido e enviado para processamento.",
                "message_id": response["MessageId"],
            },
            ensure_ascii=False,
        ),
    }
