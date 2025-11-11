import re

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and replace the send_invite block
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Look for the msg = Message line in send_invite
    if "msg = Message(subject, recipients=[app_data.email], body=body)" in line and i > 415:
        # Check if this is in send_invite (before update_status definition)
        context_before = "".join(lines[max(0, i-10):i])
        if "def send_invite" in context_before and "def update_status" not in context_before:
            # Replace mail.send block
            if i + 4 < len(lines) and "mail.send(msg)" in lines[i+1]:
                # Skip old code and add new code
                new_lines.append("        # Use centralized helper (prefers SendGrid Web API; falls back to SMTP)\n")
                new_lines.append("        send_email(app_data.email, subject, body)\n")
                i += 2  # Skip msg line and mail.send line
                continue
    new_lines.append(line)
    i += 1

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Fixed send_invite")
