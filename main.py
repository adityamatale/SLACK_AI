from langchain_core.prompts import PromptTemplate
from SLLACK.system_prompt import sys_prompt
from slack_sdk import WebClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json, os

print("Loaded main.py")


# ---------------- CONFIG ----------------
load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature=0.4)


# ---------------- PERSONALITIES ----------------
#can later make these dynamic
user_A = "Direct, logical, prefers short messages."
user_B = "Calm, dislikes reminders, prefers collaborative and supportive tone."

# ---------------- LLM ----------------
def get_ai_suggestions(user_msg: str):

    prompt = PromptTemplate(
        template = sys_prompt,
        input_variables = ["user_A", "user_B", "user_msg"]
    )
    
    with open("system_prompt.txt", "w") as f:
        f.write(sys_prompt)

    chain = prompt | llm
    response = chain.invoke({"user_A": user_A, "user_B": user_B, "user_msg": user_msg})

    # Parse AI JSON output safely
    try:
        # Extract content from AIMessage
        content = response.content if hasattr(response, 'content') else str(response)
        ai_text = content.strip()
        result = json.loads(ai_text)
        # Save response for debugging
        with open("ai_response.txt", "w") as f:
            json.dump(result, f, indent=4)
        return result["suggestions"], result["check"]

    except Exception as e:
        print("Error parsing AI response:", e)
        # fallback if JSON parsing fails
        return [
            "(AI) Maybe say: Hope your work is going well — reminder about today’s deadline.",
            "(AI) Perhaps try: The deadline is today, let me know if I can help.",
            "(AI) Try: Just checking in kindly, today’s the deadline — all good?"
        ], "yes"


# Slack user_B ID 
def get_user_id(identifier: str):
    try:
        resp = client.users_list()
        members = resp["members"]
        with open('slack_users.json', 'w') as f:
            json.dump(members, f, indent=4)
        print(f"[INFO] Fetched {len(members)} users from Slack.")
        for m in members:
            profile = m.get("profile", {})
            print(profile.get("real_name"))

        for m in members:
            profile = m.get("profile", {})

            # Match by email
            if profile.get("real_name") == identifier:
                print('--------------',m['id'], type(m['id']))
                return m["id"]

            # # Match by real name
            # if profile.get("real_name") == identifier:
            #     return m["id"]

            # # Match by display name
            # if profile.get("display_name") == identifier:
            #     return m["id"]

        print(f"[WARN] No match for: {identifier}")
        return None

    except Exception as e:
        print("Error fetching user list:", e)
        return None

