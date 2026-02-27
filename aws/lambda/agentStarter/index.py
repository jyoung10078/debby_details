import json
import os
import openai

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt", "Say something interesting.")

        # Use correct model name: gpt-4o-mini (not gpt-4-mini)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fixed: was "gpt-4-mini"
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