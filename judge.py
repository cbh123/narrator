import os
from openai import OpenAI
import base64
import json
import time
import simpleaudio as sa

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def analyze_posture(base64_image):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """
                You are a posture rater.
                I send you a profile photo of a person and you tell me roughly how their posture is.
                It's ok if you can't see the side view of the person.
                """,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "How is my posture?"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


def summarize_analysis(analysis):
    summary_response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
                You are a posture rater.
                You received an analysis of someone's posture, and you have to summarize it with a numerical rating 1-10.
                It's okay if you can't see the side view of the person, or if the analysis is inconclusive. You must give a 1-10 rating.

                Respond in JSON, with a "rating": 1-10, "reason": "...", and "conclusive": true/false (whether or not the analysis was conclusive)
                """,
            },
            {
                "role": "user",
                "content": analysis,
            }
        ],
        max_tokens=300,
    )
    return summary_response.choices[0].message.content


def main():
    while True:
        print("🧘 Judging posture...")

        # path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        # analyze posture
        analysis = analyze_posture(base64_image)

        # summarize analysis
        result = summarize_analysis(analysis)
        result_json = json.loads(result)

        print(result_json)

        # play appropriate audio file based on rating
        if result_json['rating'] <= 5:
            play_audio('./assets/stop_slouching.wav')
        else:
            play_audio('./assets/wonderful_posture.wav')

        # wait for 30 seconds
        time.sleep(5)

if __name__ == "__main__":
    main()
