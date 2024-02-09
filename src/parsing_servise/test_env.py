import os
import dotenv
dotenv.load_dotenv()
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

print(EMAIL_HOST_USER)
print(EMAIL_HOST_PASSWORD)

print(eval(os.getenv("EMAIL_USE_TLS")))