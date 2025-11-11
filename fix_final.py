import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern 1: Replace Message + mail.send in send_invite
pattern1 = r'(\s+)msg = Message\(subject, recipients=\[app_data\.email\], body=body\)\n\s+mail\.send\(msg\)'
replacement1 = r'\1# Use centralized helper (prefers SendGrid Web API; falls back to SMTP)\n\1send_email(app_data.email, subject, body)'

content = re.sub(pattern1, replacement1, content)

# Pattern 2: Replace Message + mail.send in update_status  
pattern2 = r'if status == .Accepted. and mail:\n\s+subject = "Update on your application"\n\s+body = f"Congratulations[^"]*"\n\s+msg = Message\(subject, recipients=\[app_data\.email\], body=body\)\n\s+mail\.send\(msg\)'
replacement2 = '''if status == 'Accepted':
            subject = "Update on your application"
            body = f"Congratulations! We would like to invite you to our office for the next round of interviews for the {app_data.title} role."
            try:
                send_email(app_data.email, subject, body)
            except Exception as e:
                print(f"Warning: failed to send status email: {e}")'''

content = re.sub(pattern2, replacement2, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed both blocks")
