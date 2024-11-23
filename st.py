import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Function to generate a placeholder Google Meet link
def generate_google_meet_link():
    random_id = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    return f"https://meet.google.com/{random_id}"

# Email sending function
def send_email(doctor_email, doctor_name, patient_name, disease, appointment_time, meet_link):
    sender_email = "saiakhilambati7@gmail.com"
    sender_password = "frpw fakq eyte pzqk"  # Use App Passwords for Gmail
    subject = "New Appointment Booked"
    message = f"""
    Hello Dr. {doctor_name},

    You have a new appointment booked with the following details:
    - Patient Name: {patient_name}
    - Disease: {disease}
    - Appointment Time: {appointment_time}
    - Google Meet Link: {meet_link}

    Please attend the meeting at the scheduled time.

    Best Regards,
    Your Appointment System
    """

    try:
        # Set up email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = doctor_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the email server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        st.success(f"Email sent successfully to Dr. {doctor_name}!")
    except Exception as e:
        st.error("Failed to send email.")
        st.error(str(e))

# Streamlit interface
st.title("Patient-Doctor Appointment System")

# Patient/Doctor selection
user_type = st.radio("Who are you?", ["Patient", "Doctor"])

if user_type == "Patient":
    st.header("Book an Appointment")
    
    # Patient details
    patient_name = st.text_input("Enter your name:")
    disease = st.text_input("Enter your disease/concern:")

    # List of doctors (pre-defined)
    doctors = [
        {"name": "Dr. John Smith", "specialty": "Cardiologist", "email": "saiakhilambati7@gmail.com"},
        {"name": "Dr. Emily Brown", "specialty": "Dentist", "email": "emilybrown@example.com"},
        {"name": "Dr. Sarah Wilson", "specialty": "Dermatologist", "email": "sarahwilson@example.com"},
        {"name": "Dr. Michael Johnson", "specialty": "Neurologist", "email": "michaeljohnson@example.com"}
    ]

    # Show doctors as options
    doctor_selected = st.selectbox(
        "Choose a doctor:",
        [f"{doc['name']} - {doc['specialty']}" for doc in doctors]
    )

    # Extract selected doctor's details
    doctor_index = [f"{doc['name']} - {doc['specialty']}" for doc in doctors].index(doctor_selected)
    selected_doctor = doctors[doctor_index]

    # Time selection
    time_slots = ["09:00 AM", "10:30 AM", "11:00 AM", "02:00 PM", "03:30 PM"]
    appointment_time = st.selectbox("Choose an appointment time:", time_slots)

    # Generate Google Meet link
    meet_link = generate_google_meet_link()

    # Confirmation button
    if st.button("Confirm Appointment"):
        if not patient_name or not disease:
            st.error("Please fill in all the required fields.")
        else:
            send_email(
                selected_doctor['email'],
                selected_doctor['name'],
                patient_name,
                disease,
                appointment_time,
                meet_link
            )
            st.write(f"Your appointment with Dr. {selected_doctor['name']} is confirmed!")
            st.write(f"Google Meet Link: [Join Meeting]({meet_link})")

elif user_type == "Doctor":
    st.header("Doctor Login")

    # Doctor authentication (pre-defined password)
    password = st.text_input("Enter your password:", type="password")
    correct_password = "doctor123"

    if st.button("Login"):
        if password == correct_password:
            st.success("Welcome, Doctor!")
            st.write("This section can display your upcoming appointments, patient details, etc.")
        else:
            st.error("Incorrect password.")
