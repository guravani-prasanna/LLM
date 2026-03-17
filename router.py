import os
import json
import logging
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Force simulation mode (no API calls)
client = None
print("Running in simulation mode.")

# Paths
PROMPTS_FILE = os.path.join(os.path.dirname(__file__), "prompts.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "route_log.jsonl")


def load_prompts() -> Dict[str, str]:
    """Loads expert system prompts from JSON file."""
    with open(PROMPTS_FILE, "r") as f:
        return json.load(f)


def log_interaction(intent: str, confidence: float, user_message: str, final_response: str):
    """Logs the interaction to a JSON Lines file."""
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def classify_intent(message: str) -> Dict[str, Any]:
    """
    Classifies the user message intent.
    """
    system_prompt = (
        "Your task is to classify the user's intent. Choose one of: "
        "code, data, writing, career, unclear. Return JSON with intent and confidence."
    )

    if not client:
        lower_msg = message.lower()

        if any(word in lower_msg for word in ["sort", "python", "function", "bug", "code"]):
            return {"intent": "code", "confidence": 0.95}

        elif any(word in lower_msg for word in ["data", "pivot", "average", "numbers", "sql"]):
            return {"intent": "data", "confidence": 0.92}

        elif any(word in lower_msg for word in ["paragraph", "writing", "sentence", "coach", "verbose", "poem"]):
            return {"intent": "writing", "confidence": 0.90}

        elif any(word in lower_msg for word in ["job", "career", "interview", "resume", "cover letter"]):
            return {"intent": "career", "confidence": 0.90}

        else:
            return {"intent": "unclear", "confidence": 0.50}

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"Error in classify_intent: {e}")

        # fallback
        lower_msg = message.lower()

        if any(word in lower_msg for word in ["sort", "python", "function", "bug", "code"]):
            return {"intent": "code", "confidence": 0.95}

        elif any(word in lower_msg for word in ["data", "pivot", "average", "numbers", "sql"]):
            return {"intent": "data", "confidence": 0.92}

        elif any(word in lower_msg for word in ["paragraph", "writing", "sentence", "coach", "verbose", "poem"]):
            return {"intent": "writing", "confidence": 0.90}

        elif any(word in lower_msg for word in ["job", "career", "interview", "resume", "cover letter"]):
            return {"intent": "career", "confidence": 0.90}

        else:
            return {"intent": "unclear", "confidence": 0.50}


def route_and_respond(message: str, intent_data: Dict[str, Any]) -> str:
    """
    Routes the message to the appropriate persona and returns the response.
    """
    intent = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)

    if confidence < 0.7:
        intent = "unclear"

    prompts = load_prompts()

    if intent == "unclear":
        final_response = prompts.get(
            "unclear",
            "Could you please tell me more about what you need?"
        )

    elif not client:
        # Simulation responses
        if intent == "code":
            final_response = """Here is a Python example to sort a list:

nums = [3, 1, 5, 2]
sorted_nums = sorted(nums)
print(sorted_nums)"""

        elif intent == "data":
            final_response = """To calculate the average, sum all values and divide by count.

You can visualize data using charts like bar graphs or pie charts."""

        elif intent == "writing":
            final_response = """Clouds drift softly through the sky,
Whispering dreams as they pass by.
Silver edges, calm and light,
Painting stories in the height."""

        elif intent == "career":
            final_response = """Start by defining your career goals.

Then build skills, create a strong resume, and practice interviews regularly."""

        else:
            final_response = """Could you clarify if you need help with coding, data, writing, or career advice?"""

    else:
        system_prompt = prompts.get(intent)

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            )
            final_response = response.choices[0].message.content

        except Exception as e:
            print(f"Error in route_and_respond: {e}")
            final_response = "I encountered an error. Please try again."

    log_interaction(intent, confidence, message, final_response)

    return final_response


if __name__ == "__main__":
    msg = "how do i sort a list in python?"
    intent_info = classify_intent(msg)
    print(f"Detected Intent: {intent_info}")
    res = route_and_respond(msg, intent_info)
    print(f"Response: {res}")