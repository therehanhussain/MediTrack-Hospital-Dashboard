import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

st.set_page_config(page_title="MediTrack Dashboard", page_icon="🏥", layout="wide")

st.title("🏥 MediTrack")
st.caption("Hospital Patient Management System | SQL + Python + Streamlit")

# Connection settings are entered by the user; no credentials are hardcoded.
with st.sidebar:
    st.header("Database Connection")
    db_host = st.text_input("MySQL Host", value="localhost")
    db_port = st.number_input("Port", min_value=1, max_value=65535, value=3306)
    db_user = st.text_input("MySQL Username", value="root")
    db_password = st.text_input("MySQL Password", type="password")
    db_name = st.text_input("Database Name", value="MediTrack")
    connect_clicked = st.button("Connect to MediTrack", type="primary")

if "db_config" not in st.session_state:
    st.session_state.db_config = None
if connect_clicked:
    st.session_state.db_config = {
        "host": db_host,
        "port": int(db_port),
        "user": db_user,
        "password": db_password,
        "database": db_name,
    }

if not st.session_state.db_config:
    st.info("Enter your MySQL details in the sidebar and click **Connect to MediTrack**.")
    st.markdown("""
    ### Dashboard modules
    - Overview: key counts and billing summary
    - Patients: search and view patient records
    - Doctors & Departments: doctor directory and department assignments
    - Appointments: appointment history and status summary
    - Prescriptions: prescription records
    - Billing: bills, payment methods, and balances

    This dashboard reads the existing database. It does not insert, update, or delete records.
    """)
    st.stop()

@st.cache_data(ttl=30, show_spinner=False)
def load_table(config_items, table_name):
    # Table names below are selected from a fixed allow-list in the app.
    conn = mysql.connector.connect(**dict(config_items))
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}`")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()

@st.cache_data(ttl=30, show_spinner=False)
def load_query(config_items, query):
    conn = mysql.connector.connect(**dict(config_items))
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

config_items = tuple(sorted(st.session_state.db_config.items()))

try:
    # Load the five original project tables, using only existing database rows.
    patients = load_table(config_items, "Patients")
    doctors = load_table(config_items, "Doctors")
    appointments = load_table(config_items, "Appointments")
    prescriptions = load_table(config_items, "Prescriptions")
    billing = load_table(config_items, "Billing")

    departments = None
    try:
        departments = load_table(config_items, "Departments")
    except Error:
        pass

    page = st.sidebar.radio(
        "Navigate",
        ["Overview", "Patients", "Doctors & Departments", "Appointments", "Prescriptions", "Billing"]
    )

    if st.sidebar.button("Refresh data"):
        st.cache_data.clear()
        st.rerun()

    if page == "Overview":
        st.subheader("Hospital Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Patients", len(patients))
        c2.metric("Doctors", len(doctors))
        c3.metric("Appointments", len(appointments))
        c4.metric("Prescriptions", len(prescriptions))

        total_billed = pd.to_numeric(billing.get("Amount", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()
        st.metric("Total Billing Amount", f"₹{total_billed:,.2f}")

        left, right = st.columns(2)
        with left:
            st.markdown("#### Appointments by status")
            if "Status" in appointments.columns and not appointments.empty:
                status_counts = appointments["Status"].fillna("Unknown").value_counts().rename_axis("Status").reset_index(name="Count")
                st.bar_chart(status_counts.set_index("Status"))
            else:
                st.info("No status column or appointment records found.")

        with right:
            st.markdown("#### Bills by payment method")
            if "Payment_Method" in billing.columns and not billing.empty:
                payment_counts = billing["Payment_Method"].fillna("Unknown").value_counts().rename_axis("Payment Method").reset_index(name="Count")
                st.bar_chart(payment_counts.set_index("Payment Method"))
            else:
                st.info("No payment-method column or bill records found.")

        st.markdown("#### Recent appointments")
        if "Appointment_Date" in appointments.columns:
            appointments["Appointment_Date"] = pd.to_datetime(appointments["Appointment_Date"], errors="coerce")
            st.dataframe(appointments.sort_values("Appointment_Date", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.dataframe(appointments, use_container_width=True, hide_index=True)

    elif page == "Patients":
        st.subheader("Patient Records")
        st.caption("Search uses records already stored in the MediTrack database.")
        search = st.text_input("Search by patient name, ID, email, or contact")
        filtered = patients.copy()
        if search:
            mask = pd.Series(False, index=filtered.index)
            for col in ["Patient_ID", "Name", "Email", "Contact"]:
                if col in filtered.columns:
                    mask |= filtered[col].astype(str).str.contains(search, case=False, na=False)
            filtered = filtered[mask]
        st.write(f"Records shown: {len(filtered)}")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

    elif page == "Doctors & Departments":
        st.subheader("Doctors & Departments")
        if departments is not None:
            st.markdown("#### Departments")
            st.dataframe(departments, use_container_width=True, hide_index=True)
        st.markdown("#### Doctors")
        if "Department_ID" in doctors.columns and departments is not None and "Department_ID" in departments.columns:
            dept_name_col = "Department_Name" if "Department_Name" in departments.columns else None
            if dept_name_col:
                doctor_view = doctors.merge(
                    departments[["Department_ID", dept_name_col]],
                    on="Department_ID", how="left"
                )
                st.dataframe(doctor_view, use_container_width=True, hide_index=True)
            else:
                st.dataframe(doctors, use_container_width=True, hide_index=True)
        else:
            st.dataframe(doctors, use_container_width=True, hide_index=True)
        if "Specialization" in doctors.columns and not doctors.empty:
            st.markdown("#### Doctors by specialization")
            counts = doctors["Specialization"].fillna("Unknown").value_counts().rename_axis("Specialization").reset_index(name="Doctors")
            st.bar_chart(counts.set_index("Specialization"))

    elif page == "Appointments":
        st.subheader("Appointments")
        filtered = appointments.copy()
        if "Status" in filtered.columns:
            statuses = ["All"] + sorted(filtered["Status"].dropna().astype(str).unique().tolist())
            chosen = st.selectbox("Filter by status", statuses)
            if chosen != "All":
                filtered = filtered[filtered["Status"].astype(str) == chosen]
        st.write(f"Records shown: {len(filtered)}")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

    elif page == "Prescriptions":
        st.subheader("Prescription Records")
        st.dataframe(prescriptions, use_container_width=True, hide_index=True)

    elif page == "Billing":
        st.subheader("Billing & Payments")
        billing_view = billing.copy()
        if "Amount" in billing_view.columns:
            billing_view["Amount"] = pd.to_numeric(billing_view["Amount"], errors="coerce")
            st.metric("Total billed", f"₹{billing_view['Amount'].fillna(0).sum():,.2f}")
        if "Paid_Amount" in billing_view.columns:
            billing_view["Paid_Amount"] = pd.to_numeric(billing_view["Paid_Amount"], errors="coerce")
            st.metric("Total paid", f"₹{billing_view['Paid_Amount'].fillna(0).sum():,.2f}")
        if "Balance_Amount" in billing_view.columns:
            billing_view["Balance_Amount"] = pd.to_numeric(billing_view["Balance_Amount"], errors="coerce")
            st.metric("Outstanding balance", f"₹{billing_view['Balance_Amount'].fillna(0).sum():,.2f}")
        if "Payment_Method" in billing_view.columns:
            st.markdown("#### Bills by payment method")
            pay_counts = billing_view["Payment_Method"].fillna("Unknown").value_counts().rename_axis("Payment Method").reset_index(name="Bills")
            st.bar_chart(pay_counts.set_index("Payment Method"))
        st.dataframe(billing_view, use_container_width=True, hide_index=True)

except Error as e:
    st.error("Could not connect to or read the MediTrack database.")
    st.code(str(e))
    st.markdown("""
    **Check these items:**
    1. MySQL80 service is running.
    2. MySQL Workbench can connect using the same host, port, username and password.
    3. The database name is `MediTrack`.
    4. The tables are named `Patients`, `Doctors`, `Appointments`, `Prescriptions`, and `Billing`.
    """)
except Exception as e:
    st.error("Something went wrong while loading the dashboard.")
    st.code(str(e))
