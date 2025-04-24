from openai import OpenAI


# source: https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key?api-mode=responses&lang=python

def main():
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "user", "content": "what teams are playing in this image?"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": ""
                    }
                ]
            }
        ]
    )

print(response.output_text)

if __name__ == "__main__":
    main()
