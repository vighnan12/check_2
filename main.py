from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# ✅ Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ Hardcoded Gmail credentials (test only!)
GMAIL_USER = "becines84@gmail.com"
GMAIL_APP_PASSWORD = "bfnb kqqn dmpw txzq"  # App Password

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str

@app.post("/send-email")
def send_email(request: EmailRequest):
    try:
        msg = MIMEText(request.body)
        msg["Subject"] = request.subject
        msg["From"] = GMAIL_USER
        msg["To"] = request.to

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, [request.to], msg.as_string())

        return {"success": True, "message": f"Email sent to {request.to}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
