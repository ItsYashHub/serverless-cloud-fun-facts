import boto3
import random
import json

# DynamoDB table: CloudFacts (FactID, FactText)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CloudFacts")

# Bedrock client (region must match your Bedrock / Lambda region)
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

def lambda_handler(event, context):
    # 1. Fetch all facts from DynamoDB
    response = table.scan()
    items = response.get("Items", [])
    if not items:
        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": json.dumps({"fact": "No facts available in DynamoDB."})
        }

    # 2. Pick random fact
    base_fact = random.choice(items).get("FactText", "No FactText found")

    # 3. Ask Bedrock (Claude 3.5 Sonnet) to make it witty
    messages = [
        {
            "role": "user",
            "content": f"Take this cloud computing fact and make it fun and engaging in 1–2 sentences maximum. Keep it short and witty: {base_fact}"
        }
    ]

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": messages,
        "temperature": 0.7,
    }

    witty_fact = base_fact  # fallback
    try:
        resp = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )
        result = json.loads(resp["body"].read())
        if "content" in result and result["content"]:
            for block in result["content"]:
                if block.get("type") == "text":
                    text = block["text"].strip()
                    if text:
                        witty_fact = text
                        break
    except Exception as e:
        print(f"Bedrock error: {e}")
        # fallback to base_fact

    return {
        "statusCode": 200,
        "headers": _cors_headers(),
        "body": json.dumps({"fact": witty_fact})
    }


def _cors_headers():
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
