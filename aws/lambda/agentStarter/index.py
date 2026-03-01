import json
import os
import openai

# make sure we actually have a key; deploying without one results in a
# confusing 401 from the OpenAI API, so fail fast and give a clear log
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    # Lambda initialisation happens once, so raising here will cause the
    # function to fail early and the error will appear in CloudWatch.
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

client = openai.OpenAI(api_key=api_key)

def lambda_handler(event, context):
    try:
        # Parse the request body; API Gateway may supply None for body when
        # no payload is sent, so guard against that case.
        raw = event.get("body")
        if raw is None:
            raw = "{}"
        body = json.loads(raw)
        prompt = body.get("prompt", body)

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