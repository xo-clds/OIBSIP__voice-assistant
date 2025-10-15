import os
import speech_recognition as sr
from openai import OpenAI

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
client = OpenAI(api_key=api_key)

# Initialize recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Predefined command responses
predefined_responses = {
    "what is your name": "I am your personal AI assistant.",
    "who are you": "I am an AI created to assist you with information and tasks.",
    "what do you do": "I can answer your questions, help with tasks, or just chat with you.",
    "how could you help me": "I can provide information, suggestions, or just keep you company!",
    "stop": "Exiting the assistant. Goodbye!"
}

print("Listening... Say 'stop' to quit.")

while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("\nSpeak something:")
            audio = recognizer.listen(source)

        # Convert speech to text
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)

        # Check predefined responses first
        if text in predefined_responses:
            answer = predefined_responses[text]
            print("AI:", answer)
            if text == "stop":
                break
        else:
            # Send other text to OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": text}]
            )
            answer = response.choices[0].message.content
            print("AI:", answer)

    except sr.UnknownValueError:
        print(" Could not understand audio. Try again.")
    except sr.RequestError as e:
        print(f" Could not request results; {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
        break
