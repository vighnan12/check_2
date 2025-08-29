from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sendgrid
from sendgrid.helpers.mail import Mail

# ⚠️ Normally store this in ENV VARS, not hardcoded!
SENDGRID_API_KEY = "SG.8IWimK8SSvK9la06S5l9_w.WUaIsf95SzNtwaNUdi6-1Q3Qlc5-8m_1MaYQ9Oa1tb4"

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email request model
class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str

@app.post("/send-email")
async def send_email(email: EmailRequest):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        message = Mail(
            from_email="vighnankumarmanuwada@gmail.com",  # ✅ Your verified sender
            to_emails=email.to,
            subject=email.subject,
            html_content=email.html,
        )

        response = sg.send(message)
        return {
            "success": True,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.body.decode() if response.body else None,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
async def root():
    return {"message": "🚀 SendGrid Email API running!"}
