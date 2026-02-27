import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt", "Say something interesting.")

        # Use correct OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": response.choices[0].message.content
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }