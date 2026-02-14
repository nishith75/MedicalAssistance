from src.chatbot.semantic_search import search_medical_query


# ---------- FORMAT RESPONSE ----------
def format_response(results):
    if not results:
        return "Sorry, I couldn't find relevant information.", None

    response = "\n\nHere is some general medical information:\n"
    response += "=" * 50 + "\n"

    detected_disease = None

    for r in results:
        parts = r.split("Symptoms:")
        disease_part = parts[0].replace("Disease:", "").strip()

        detected_disease = disease_part  # store disease for memory

        symptoms_part = parts[1].split("Prevention:")[0].strip()
        prevention_part = parts[1].split("Prevention:")[1].split("Common solutions:")[0].strip()
        solutions_part = parts[1].split("Common solutions:")[1].strip()

        response += f"\n🩺 Disease: {disease_part}\n"

        response += "\n🔹 Symptoms:\n"
        for symptom in symptoms_part.split(","):
            response += f"  • {symptom.strip()}\n"

        response += "\n🔹 Prevention:\n"
        for prevention in prevention_part.split(","):
            response += f"  • {prevention.strip()}\n"

        response += "\n🔹 General Care:\n"
        for solution in solutions_part.split(","):
            response += f"  • {solution.strip()}\n"

        response += "\n" + "-" * 50 + "\n"

    response += "\n⚠ Disclaimer: This information is for awareness only and not medical advice.\n"
    return response, detected_disease


# ---------- EMERGENCY CHECK ----------
def check_emergency(user_input):
    emergency_keywords = [
        "chest pain",
        "breathing difficulty",
        "unconscious",
        "severe bleeding",
        "heart attack",
        "stroke",
        "not breathing",
        "seizure"
    ]

    for word in emergency_keywords:
        if word in user_input.lower():
            return True
    return False


# ---------- CHATBOT LOOP WITH MEMORY ----------
def run_chatbot():
    print("\n🩺 Medical Awareness Chatbot")
    print("Type 'exit' to quit.\n")

    last_disease = None  # memory variable

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Stay healthy! 👋")
            break

        if check_emergency(user_input):
            print("\n🚨 EMERGENCY ALERT 🚨")
            print("Your symptoms may indicate a medical emergency.")
            print("Please seek immediate medical attention or call emergency services.\n")
            continue

        # Handle follow-up questions
        if last_disease and any(word in user_input.lower() for word in ["serious", "dangerous", "curable"]):
            print(f"\nBot: {last_disease} is usually manageable with proper care. "
                  f"If symptoms worsen, consult a medical professional.\n")
            continue

        results = search_medical_query(user_input)
        reply, detected = format_response(results)

        last_disease = detected  # update memory

        print("\nBot:", reply)


if __name__ == "__main__":
    run_chatbot()
