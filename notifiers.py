
from email.message import EmailMessage
import smtplib
import ssl

from plyer import notification


def notifyDesktop(title):
    notification.notify(
        title='this is crazy',
        message='This is a notification message.',
        app_name='My App',
        timeout=10  # Duration in seconds
    )

def notifyEmail(title):
    
    message = EmailMessage()
    message.set_content('https://job-boards.greenhouse.io/growtherapy?offices%5B%5D=4011317005')

    # me == the sender's email address
    # you == the recipient's email address
    message['Subject'] = f'job time'
    message['From'] = "robert.gugliel@gmail.com"
    message['To'] = "robert.gugliel@gmail.com"

    # Create secure SSL/TLS context
    context = ssl.create_default_context()

    try:
        # For Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        
        print("Connecting to server...")
        server.starttls(context=context)  # Enable TLS with secure context
        
        print("Logging in...")
        server.login("robert.gugliel@gmail.com", "PUT YOUR PASSWORD HERE")
        
        print("Sending email...")
        server.send_message(message)
        print("Email sent successfully!")
        
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email and password.")
        print("If using Gmail, make sure you're using an App Password.")
    except ConnectionRefusedError:
        print("Connection refused. Please check:")
        print("1. Your internet connection")
        print("2. Firewall settings")
        print("3. Antivirus settings")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            server.quit()
        except:
            pass

