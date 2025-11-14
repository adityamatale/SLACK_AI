from pathlib import Path
import sys
original_sys_path = sys.path.copy()
# Two directories above
two_up = Path(__file__).resolve().parents[2]
print(two_up)
sys.path.append(str(two_up))

from main import get_ai_suggestions, get_user_id
sys.path = original_sys_path
from fastapi import APIRouter, Request
from slack_sdk import WebClient
from dotenv import load_dotenv
import json, os

# config
load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
router = APIRouter()
USER_B_IDENTIFIER = os.getenv("USER_B_IDENTIFIER")

# ---------------- EVENT HANDLER ----------------
@router.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()

    # Slack verification
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    # Handle incoming messages
    if "event" in data and data["event"]["type"] == "message":
        event = data["event"]
        if event.get("user") and not event.get("bot_id"):
            user_a_id = event["user"]
            user_msg = event["text"]

            # 1. Get empathetic suggestions
            suggestions, check = get_ai_suggestions(user_msg)
            user_b_id = get_user_id(USER_B_IDENTIFIER)
            print(f"[INFO] User A ID: {user_a_id}, User B ID: {user_b_id}")
            
            if check == "no":
                # If message is appropriate, no action needed

                # Confirm to User A
                client.chat_postMessage(
                    channel=user_a_id,
                    text=f"✅ Sent this message to User B:\n> {user_msg}"
                )

                # Forward to User B
                client.chat_postMessage(
                    channel=user_b_id,
                    text=f"💬 *From User A*: {user_msg}"
                )


                return {"ok": True}

            # 2. Build Slack buttons dynamically
            blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": "*AI Suggestions:*"}}]
            for i, s in enumerate(suggestions):
                blocks.append({
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{s}"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Send this"},
                        "value": json.dumps({"msg": s, "userA": user_a_id})
                    }
                })

            # 3. Send message to User A (DM)
            client.chat_postMessage(
            channel=user_a_id,
            text="Message suggestions from AI",  
            blocks=blocks
            )

    return {"ok": True}

# ---------------- INTERACTION HANDLER ----------------
@router.post("/slack/interactions")
async def slack_interactions(request: Request):
    form_data = await request.form()
    payload = json.loads(form_data["payload"])
    action = payload["actions"][0]
    value = json.loads(action["value"])
    selected_msg = value["msg"]
    user_a_id = value["userA"]

    user_b_id = get_user_id(USER_B_IDENTIFIER)
    print(f"[INFO] Interaction - User A ID: {user_a_id}, User B ID: {user_b_id}")

    # Confirm to User A
    client.chat_postMessage(
        channel=user_a_id,
        text=f"✅ Sent this message to User B:\n> {selected_msg}"
    )

    # Forward to User B
    client.chat_postMessage(
        channel=user_b_id,
        text=f"💬 *From User A*: {selected_msg}"
    )

    return {"ok": True}