import logging
import azure.functions as func
import psycopg2

def main(msg: func.ServiceBusMessage):
    notification_id = msg.get_body().decode('utf-8')
    logging.info(f"Processing notification_id: {notification_id}")

    # Database connection
    conn = psycopg2.connect(
        dbname='techconfdb',
        user='pgadmin',
        password='Coverlink2803',
        host='pg-west-us2.postgres.database.azure.com',
        port='5432'
    )
    cursor = conn.cursor()

    # Query to retrieve the subject and message
    cursor.execute("SELECT subject, message FROM notifications WHERE id = %s", (notification_id,))
    subject, message = cursor.fetchone()

    # Query to retrieve attendees
    cursor.execute("SELECT email, first_name FROM attendees WHERE notification_id = %s", (notification_id,))
    attendees = cursor.fetchall()

    total_notified = 0

    # Loop through attendees and send personalized messages
    for email, first_name in attendees:
        personalized_message = f"Hello {first_name}, {message}"
        # Here you would send the email (using an email service)
        # send_email(email, subject, personalized_message)
        total_notified += 1

    # Update notification status
    cursor.execute("UPDATE notifications SET status = 'Notified', total_attendees_notified = %s WHERE id = %s", (total_notified, notification_id))
    conn.commit()

    cursor.close()
    conn.close()
    logging.info(f"Total attendees notified: {total_notified}")
