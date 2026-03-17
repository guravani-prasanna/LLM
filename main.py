import sys
import argparse
from router import classify_intent, route_and_respond

TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]

def run_tests():
    print("="*50)
    print("RUNNING SYSTEM TESTS")
    print("="*50)
    
    for i, msg in enumerate(TEST_MESSAGES, 1):
        print(f"\nTest Case {i}: \"{msg}\"")
        intent_info = classify_intent(msg)
        print(f"Detected Intent: {intent_info['intent']} (Confidence: {intent_info['confidence']})")
        
        response = route_and_respond(msg, intent_info)
        print(f"Final Response: {response[:100]}...") # Print first 100 chars
        print("-" * 30)

def main():
    parser = argparse.ArgumentParser(description="Prompt Router CLI")
    parser.add_argument("--test", action="store_true", help="Run the predefined 15 test cases")
    parser.add_argument("--msg", type=str, help="Single message to route and respond")
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    elif args.msg:
        intent_info = classify_intent(args.msg)
        print(f"Intent: {intent_info}")
        print(f"Response: {route_and_respond(args.msg, intent_info)}")
    else:
        print("Welcome to the Prompt Router. Enter your message (or type 'exit' to quit):")
        while True:
            try:
                user_input = input("> ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                intent_info = classify_intent(user_input)
                print(f"[System] Intent: {intent_info['intent']} ({intent_info['confidence']:.2f})")
                
                response = route_and_respond(user_input, intent_info)
                print(f"\n{response}\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
