import streamlit as st
from difflib import get_close_matches
from datetime import datetime

# Store user session info
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "industry" not in st.session_state:
    st.session_state.industry = ""
if "needs" not in st.session_state:
    st.session_state.needs = []
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Command keywords
command_keywords = {
    "help": ["help", "support", "assist", "issue"],
    "info": ["info", "information", "about"],
    "contact": ["contact", "email", "reach"],
    "services": ["services", "service", "offerings"],
    "faq": ["faq", "questions", "answers"],
    "demo": ["demo", "demonstration", "show"],
    "portfolio": ["portfolio", "examples", "work", "clients"],
    "summary": ["summary", "report", "download"],
    "exit": ["exit", "quit", "bye"]
}

def match_keyword(user_input):
    user_input = user_input.lower()
    for key, phrases in command_keywords.items():
        for phrase in phrases:
            if phrase in user_input:
                return key
            match = get_close_matches(user_input, phrases, n=1, cutoff=0.7)
            if match:
                return key
    return None

def dynamic_services(industry):
    services = {
        "construction": "We help streamline contractor scheduling, safety tracking, and automated client follow-ups.",
        "tech": "We assist with chatbot support, lead qualification, and API-based automation tools.",
        "beauty": "We offer appointment booking automation, product recommendation bots, and client follow-up messaging.",
        "default": "We provide intelligent automation, chatbot building, and custom integration to boost efficiency."
    }
    return services.get(industry.lower(), services["default"])

def dynamic_faq(industry):
    if industry.lower() == "construction":
        return "1. Can Noori schedule inspections?\n2. Can she track on-site reports?\n3. Can she follow up with clients automatically?"
    elif industry.lower() == "tech":
        return "1. Does Noori integrate with APIs?\n2. Can she be hosted on cloud platforms?\n3. Can she work with Slack or Discord?"
    elif industry.lower() == "beauty":
        return "1. Can Noori handle appointment bookings?\n2. Can she remember return clients?\n3. Can she recommend products?"
    else:
        return "1. Is Noori AI customizable?\n2. Can she grow with my business?\n3. Does she require coding knowledge?"

def handle_command(command):
    if command == "help":
        return "I'm here to assist you. You can ask me about services, demos, contact info, and more."
    elif command == "info":
        return "Noori AI is a human-friendly, customizable assistant built by Simel Noori to help companies scale smarter using automation and conversation."
    elif command == "contact":
        return "You can reach us at Simelnoori@yahoo.com. We’re happy to help!"
    elif command == "services":
        return dynamic_services(st.session_state.industry)
    elif command == "faq":
        return dynamic_faq(st.session_state.industry)
    elif command == "demo":
        return "To schedule a live demo, email Simelnoori@yahoo.com with your availability this week."
    elif command == "portfolio":
        return "We’ve built AI bots for industries including construction, e-commerce, and wellness. Recent highlight: a contractor scheduling assistant for a Chicago firm."
    elif command == "summary":
        return "A session summary will soon be available to export. Stay tuned for updates on our website!"
    elif command == "exit":
        return "exit"
    else:
        return "I'm sorry, I didn’t quite catch that. Try asking about services, FAQ, or portfolio."

# 💖 UI Layout
st.title("✨ Noori AI: Business Assistant ✨")
st.caption("Built by Simel Noori. Powered by light. Designed to scale.")

if not st.session_state.submitted:
    with st.form("user_form"):
        name = st.text_input("What’s your full name?")
        industry = st.selectbox("What industry are you in?", ["Construction", "Tech", "Beauty", "Other"])
        needs = st.multiselect(
            "What are your top business needs?",
            ["Lead generation", "Customer support", "Automation", "Appointment scheduling"]
        )
        submitted = st.form_submit_button("Start Chat")
        if submitted and name:
            st.session_state.submitted = True
            st.session_state.name = name
            st.session_state.industry = industry
            st.session_state.needs = needs
            st.success(f"Hi {name.title()}! 💬 Let's chat below.")
        elif submitted:
            st.warning("Please enter your name before continuing.")

if st.session_state.submitted:
    st.markdown("**You can type things like:** `services`, `info`, `demo`, `portfolio`, `exit`, etc.")
    user_input = st.text_input("You:", key="chat_input")

    if user_input:
        command = match_keyword(user_input)
        response = handle_command(command)

        if response == "exit":
            st.write("🛑 Session ended. Thank you for chatting with Noori AI!")
            st.markdown(f"_Session closed on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}_")
            st.session_state.submitted = False
        else:
            st.session_state.chat_log.append(("You", user_input))
            st.session_state.chat_log.append(("Noori AI", response))

    for speaker, text in st.session_state.chat_log:
        st.markdown(f"**{speaker}:** {text}")
