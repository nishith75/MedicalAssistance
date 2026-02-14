import streamlit as st
from src.chatbot.semantic_search import search_medical_query

# ---------- Emergency Detection ----------
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


# ---------- Format Response ----------
def format_response(results):
    if not results:
        return "Sorry, I couldn't find relevant information."

    response = ""

    for r in results:
        parts = r.split("Symptoms:")
        disease_part = parts[0].replace("Disease:", "").strip()

        symptoms_part = parts[1].split("Prevention:")[0].strip()
        prevention_part = parts[1].split("Prevention:")[1].split("Common solutions:")[0].strip()
        solutions_part = parts[1].split("Common solutions:")[1].strip()

        response += f"### 🩺 Disease: {disease_part}\n\n"

        response += "**🔹 Symptoms:**\n"
        for symptom in symptoms_part.split(","):
            response += f"- {symptom.strip()}\n"

        response += "\n**🔹 Prevention:**\n"
        for prevention in prevention_part.split(","):
            response += f"- {prevention.strip()}\n"

        response += "\n**🔹 General Care:**\n"
        for solution in solutions_part.split(","):
            response += f"- {solution.strip()}\n"

        response += "\n---\n"

    response += "\n⚠ *Disclaimer: This information is for awareness only and not medical advice.*"
    return response


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Medical AI Chatbot", layout="centered")

st.title("🩺 AI Medical Awareness Chatbot")
st.write("Ask about symptoms, diseases, or prevention.")

user_input = st.text_input("Enter your symptoms or question:")

if user_input:
    if check_emergency(user_input):
        st.error("🚨 This may indicate a medical emergency. Please seek immediate medical attention.")
    else:
        results = search_medical_query(user_input)
        response = format_response(results)
        st.markdown(response)
