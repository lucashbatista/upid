import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from db_connect import get_database # Import the connection function

def send_html_email(recipient_email, html_content):
    """Sends an HTML email using Python's smtplib."""
    smtp_server = "smtp.gmail.com" # Use your SMTP server (e.g., Gmail, Outlook, etc.)
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password" # Use an app password for security

    # Create the root message and set the headers
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Newsletter Subject"
    message["From"] = sender_email
    message["To"] = recipient_email

    # Attach the HTML content to the email
    message.attach(MIMEText(html_content, "html"))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Newsletter sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")

def generate_newsletter_html(subscriber_name, content_data):
    """
    Generates the HTML content for the newsletter. 
    You might use a templating engine like Jinja2 here for a real application.
    """
    html_template = f"""
    <html>
    <body>
        <h2>Hello, {subscriber_name}!</h2>
        <p>Here is your weekly update:</p>
        <ul>
            <li>{content_data.get("item1", "")}</li>
            <li>{content_data.get("item2", "")}</li>
        </ul>
        <p>Read more on our [website](http://example.com).</p>
    </body>
    </html>
    """
    return html_template

if __name__ == "__main__":
    db = get_database()
    subscribers_collection = db["subscribers"] # Assuming a 'subscribers' collection

    # Fetch subscribers from MongoDB Atlas
    # In a real scenario, you would use a query to get a list of emails
    subscribers = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"}
    ]
    
    # Example dynamic content
    newsletter_data = {"item1": "New feature released!", "item2": "Upcoming webinar on MongoDB Atlas."}

    for subscriber in subscribers:
        html_output = generate_newsletter_html(subscriber["name"], newsletter_data)
        send_html_email(subscriber["email"], html_output)

