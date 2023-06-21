import time
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def login_to_linkedin(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()
    WebDriverWait(driver, 10).until(EC.title_contains("LinkedIn"))
    return driver

def fetch_linkedin_data(driver):
    driver.get("https://www.linkedin.com/feed/")
    # Implement code to extract the necessary data from the LinkedIn profile
    unread_messages = 10
    unread_notifications = 5
    return unread_messages, unread_notifications

def compare_data(current_data, previous_data):
    # Implement code to compare the current data with the previous data
    # Calculate the differences and return the results
    message_diff = current_data[0] - previous_data[0]
    notification_diff = current_data[1] - previous_data[1]
    return message_diff, notification_diff

def create_email_body(message_diff, notification_diff):
    # Create an HTML template with placeholders for the data
    html_template = """
    <html>
    <body>
        <h1>LinkedIn Notification</h1>
        <p>Number of Unread Messages: {message_diff}</p>
        <p>Number of Unread Notifications: {notification_diff}</p>
    </body>
    </html>
    """
    # Fill in the placeholders with the actual data
    email_body = html_template.format(message_diff=message_diff, notification_diff=notification_diff)
    return email_body

def send_email_notification(email_body, recipient_email):
    sender_email = "devumang096@gmail.com"
    password = getpass.getpass("Enter your email password: ")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "LinkedIn Notification"

    msg.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")

def main():
    # Load configuration with LinkedIn users and recipient email addresses
    config = {
        "users": [
            {"username": "user1", "password": "password1"},
            {"username": "user2", "password": "password2"}
        ],
        "recipients": [
            "codespace27@gmail.com",
            "kalashshandilya@gmail.com"
        ]
    }

    # Load previous data from the Excel file
    previous_data = load_previous_data()

    for user in config["users"]:
        username = user["username"]
        password = user["password"]

        driver = login_to_linkedin(username, password)
        current_data = fetch_linkedin_data(driver)
        driver.quit()

        message_diff, notification_diff = compare_data(current_data, previous_data)

        if message_diff > 0 or notification_diff > 0:
            email_body = create_email_body(message_diff, notification_diff)

            for recipient_email in config["recipients"]:
                send_email_notification(email_body, recipient_email)

        # Update previous data for the next iteration
        previous_data = current_data

        # Wait for 3 hours before the next iteration
        time.sleep(3 * 60 * 60)

    # Save the final data to the Excel file for future usage
    save_data_to_excel(current_data)

def load_previous_data():
    # Implement code to load the previous data from the Excel file
    # Return the loaded data as a tuple (unread_messages, unread_notifications)
    return (0, 0)

def save_data_to_excel(data):
    # Implement code to save the data to an Excel file for future usage
    pass

if __name__ == "__main__":
    main()
