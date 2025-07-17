import streamlit as st
import mysql.connector
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Lagalaxy',
    database='CarRentalSystem'
)
cursor = conn.cursor()

st.title(" Car Rental System")

# -----------------------------
# Add Customer
# -----------------------------
st.header("Add Customer")
name = st.text_input("Name")
phone = st.text_input("Phone")
email = st.text_input("Email")
license_num = st.text_input("Driver's License")

if st.button("Add Customer"):
    if name and phone and email and license_num:
        try:
            cursor.execute(
                "INSERT INTO Customer (Name, Phone, Email, LicenseNumber) VALUES (%s, %s, %s, %s)",
                (name, phone, email, license_num)
            )
            conn.commit()
            st.success("Customer added.")
        except mysql.connector.Error as err:
            st.error(f" Error: {err}")
    else:
        st.warning("Please fill in all fields.")

# -----------------------------
# Create Rental
# -----------------------------
st.header("Create Rental")

# Fetch customers
cursor.execute("SELECT CustomerID, Name FROM Customer")
customers = cursor.fetchall()
if customers:
    customer_dict = {f"{name} (ID: {cid})": cid for cid, name in customers}
    selected_customer = st.selectbox("Select Customer", list(customer_dict.keys()))
else:
    st.warning(" No customers found. Add a customer first.")
    selected_customer = None

# Fetch available vehicles
cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle WHERE Status = 'Available'")
vehicles = cursor.fetchall()
if vehicles:
    vehicle_dict = {f"{make} {model} {year} (ID: {vid})": vid for vid, make, model, year in vehicles}
    selected_vehicle = st.selectbox("Select Vehicle", list(vehicle_dict.keys()))
else:
    st.warning("No available vehicles found.")
    selected_vehicle = None

# Date inputs
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if selected_customer and selected_vehicle:
    if start_date and end_date and end_date >= start_date:
        rental_days = (end_date - start_date).days or 1
        cost = rental_days * 50
        st.info(f"Rental Duration: {rental_days} day(s)")
        st.success(f"Total Cost: ${cost}")

        if st.button("Create Rental"):
            try:
                cursor.execute("""
                    INSERT INTO Rental (CustomerID, VehicleID, StartDate, EndDate, TotalCost)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    customer_dict[selected_customer],
                    vehicle_dict[selected_vehicle],
                    start_date, end_date, cost
                ))
                cursor.execute("UPDATE Vehicle SET Status = 'Rented' WHERE VehicleID = %s", 
                               (vehicle_dict[selected_vehicle],))
                conn.commit()
                st.success("Rental created and vehicle marked as Rented.")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
    else:
        st.warning(" Please choose valid start and end dates.")

# -----------------------------
# Return Vehicle
# -----------------------------
st.header("Return Vehicle")

cursor.execute("""
    SELECT R.RentalID, C.Name, V.Make, V.Model
    FROM Rental R
    JOIN Customer C ON R.CustomerID = C.CustomerID
    JOIN Vehicle V ON R.VehicleID = V.VehicleID
    WHERE V.Status = 'Rented'
    AND R.RentalID = (
        SELECT MAX(R2.RentalID)
        FROM Rental R2
        WHERE R2.VehicleID = R.VehicleID
    )
""")
active_rentals = cursor.fetchall()

if active_rentals:
    rental_options = {
        f"{rental_id} - {cust_name} ({make} {model})": rental_id
        for rental_id, cust_name, make, model in active_rentals
    }
    selected_rental = st.selectbox("Select Rental to Return", list(rental_options.keys()))

    if st.button("Return Vehicle"):
        rental_id = rental_options[selected_rental]
        cursor.execute("SELECT VehicleID FROM Rental WHERE RentalID = %s", (rental_id,))
        vehicle_id = cursor.fetchone()[0]

        cursor.execute("UPDATE Vehicle SET Status = 'Available' WHERE VehicleID = %s", (vehicle_id,))
        conn.commit()
        st.success("Vehicle returned and marked as Available.")
else:
    st.info("No rentals to return at this time.")


st.header("Record Payment")


#---------------------------------------------
# Get rentals that haven't been paid yet
#----------------------------------------
cursor.execute("""
    SELECT R.RentalID, C.Name, V.Make, V.Model, R.TotalCost
    FROM Rental R
    JOIN Customer C ON R.CustomerID = C.CustomerID
    JOIN Vehicle V ON R.VehicleID = V.VehicleID
    WHERE R.RentalID NOT IN (SELECT RentalID FROM Payment)
""")
unpaid_rentals = cursor.fetchall()

if unpaid_rentals:
    payment_dict = {
        f"{rental_id} - {cust_name} ({make} {model}) - ${total_cost:.2f}": (rental_id, total_cost)
        for rental_id, cust_name, make, model, total_cost in unpaid_rentals
    }
    selected_payment = st.selectbox("Select Rental to Pay", list(payment_dict.keys()))
    payment_method = st.selectbox("Payment Method", ["Credit", "Debit", "Cash", "Other"])
    payment_date = st.date_input("Payment Date")

    if st.button("Record Payment"):
        rental_id, amount = payment_dict[selected_payment]
        cursor.execute("""
            INSERT INTO Payment (RentalID, Amount, PaymentDate, PaymentMethod)
            VALUES (%s, %s, %s, %s)
        """, (rental_id, amount, payment_date, payment_method))
        conn.commit()
        st.success("Payment recorded successfully.")
else:
    st.info("No unpaid rentals found.")