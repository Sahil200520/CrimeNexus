import os
import sys
import pandas as pd
import streamlit as st

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from Continuous_learning_and_feedback.feedback import send_feedback_session_invitation
from Continuous_learning_and_feedback.alert import send_alert


def update_police_allocation():
    with st.expander("**Update Police Resources**", expanded=False):
        st.subheader("Police Resource Allocation Updation")

        update_needed = st.checkbox("Do you want to update the police resource allocation?")

        if update_needed:
            data_file_path = os.path.join(root_dir, 'Component_datasets', 'Resource_Allocation_Cleaned.csv')
            if not os.path.exists(data_file_path):
                st.error("Resource Allocation dataset file not found.")
                return

            df = pd.read_csv(data_file_path)
            units = sorted(df["District Name"].dropna().unique().tolist())

            if not units:
                st.error("No district units available in dataset.")
                return

            selected_unit = st.selectbox("Select the unit you want to update:", units)

            current_allocation = df[df["District Name"] == selected_unit]
            if current_allocation.empty:
                st.warning("Selected unit not found in data.")
                return

            current_asi = int(current_allocation["Sanctioned Strength of Assistant Sub-Inspectors per District"].iloc[0])
            current_chc = int(current_allocation["Sanctioned Strength of Head Constables per District"].iloc[0])
            current_cpc = int(current_allocation["Sanctioned Strength of Police Constables per District"].iloc[0])

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Current Police Resource Allocation")
                data = {"Unit": [selected_unit], "ASI": [current_asi], "CHC": [current_chc], "CPC": [current_cpc]}
                st.table(pd.DataFrame(data))

            with col2:
                st.subheader("Update Police Resource Allocation")
                new_asi = st.number_input(f"Enter new ASI count for {selected_unit}", min_value=0, step=1, value=current_asi)
                new_chc = st.number_input(f"Enter new CHC count for {selected_unit}", min_value=0, step=1, value=current_chc)
                new_cpc = st.number_input(f"Enter new CPC count for {selected_unit}", min_value=0, step=1, value=current_cpc)
                confirm_update = st.button(f"Confirm Update for {selected_unit}", type="primary")

            if confirm_update:
                df.loc[df["District Name"] == selected_unit, "Sanctioned Strength of Assistant Sub-Inspectors per District"] = new_asi
                df.loc[df["District Name"] == selected_unit, "Sanctioned Strength of Head Constables per District"] = new_chc
                df.loc[df["District Name"] == selected_unit, "Sanctioned Strength of Police Constables per District"] = new_cpc

                df.to_csv(data_file_path, index=False)
                st.success(f"Police resource allocation for {selected_unit} has been updated and saved successfully.")


def display_alert_meter(avg_rating, negative_feedback_count):
    with st.expander("**Live Feedback Monitoring and Alert Meter**", expanded=False):
        rating_threshold = 3.5
        negative_feedback_threshold = 20

        rating_percentage = min(max(avg_rating / 5.0, 0.0), 1.0)
        negative_feedback_percentage = min(max(negative_feedback_count / float(negative_feedback_threshold), 0.0), 1.0)

        st.subheader("Alert Meter")
        col1, col2 = st.columns(2)

        with col1:
            st.progress(rating_percentage, text=f"Avg. Rating: {avg_rating:.2f} / 5.00")
        with col2:
            st.progress(negative_feedback_percentage, text=f"Negative Feedback: {negative_feedback_count}/{negative_feedback_threshold}")

        rating_is_bad = (avg_rating < rating_threshold) and (avg_rating > 0)
        negative_feedback_is_high = (negative_feedback_count >= negative_feedback_threshold)

        if rating_is_bad or negative_feedback_is_high:
            st.warning("⚠️ The system feedback threshold requires attention. An alert notification has been triggered.")
            send_alert(avg_rating, rating_threshold, negative_feedback_count, negative_feedback_threshold)
        else:
            st.success("✅ System feedback levels are performing within healthy parameters.")

        st.markdown("**Note:** Automated email alert reports will be sent to engineering support when threshold criteria are breached.")


def continuous_learning_and_feedback():
    st.title("Continuous Learning and Feedback")
    st.text("Explore system feedback controls and stakeholder communication tools:")

    update_police_allocation()

    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Feedback.csv')
    if os.path.exists(data_file_path):
        try:
            feedback_df = pd.read_csv(data_file_path)
        except Exception:
            feedback_df = pd.DataFrame(columns=["Feedback Type", "Feedback Rating", "Feedback Comments"])
    else:
        feedback_df = pd.DataFrame(columns=["Feedback Type", "Feedback Rating", "Feedback Comments"])

    if not feedback_df.empty and "Feedback Rating" in feedback_df.columns:
        avg_rating = float(feedback_df["Feedback Rating"].mean())
        negative_feedback_count = len(feedback_df[feedback_df["Feedback Rating"] < 3])
    else:
        avg_rating = 5.0
        negative_feedback_count = 0

    display_alert_meter(avg_rating, negative_feedback_count)

    with st.expander("**Provide Feedback**", expanded=False):
        feedback_form = st.form(key="feedback_form")
        feedback_type = feedback_form.selectbox("Select Feedback Category", ["Crime Pattern Analysis", "Criminal Profiling", "Predictive Modeling", "Resource Allocation"])
        feedback_rating = feedback_form.slider("Rate accuracy and usefulness of output", min_value=1, max_value=5, value=4)
        feedback_comments = feedback_form.text_area("Additional Comments")
        submit_feedback = feedback_form.form_submit_button("Submit Feedback", type="primary")

        if submit_feedback:
            feedback_entry = {
                "Feedback Type": feedback_type,
                "Feedback Rating": feedback_rating,
                "Feedback Comments": feedback_comments
            }
            store_feedback_data(feedback_entry)
            st.success("Thank you! Your feedback has been recorded.")

    with st.expander("**Knowledge Base**", expanded=False):
        st.write("Recorded system feedback history:")
        display_knowledge_base(feedback_df)

    with st.expander("**Feedback Sessions Invitation**", expanded=False):
        organize_feedback_sessions()


def store_feedback_data(feedback_data):
    feedback_file_path = os.path.join(root_dir, 'Component_datasets', 'Feedback.csv')
    if os.path.exists(feedback_file_path):
        try:
            feedback_df = pd.read_csv(feedback_file_path)
            new_row = pd.DataFrame([feedback_data])
            feedback_df = pd.concat([feedback_df, new_row], ignore_index=True)
        except Exception:
            feedback_df = pd.DataFrame([feedback_data])
    else:
        feedback_df = pd.DataFrame([feedback_data])
    
    feedback_df.to_csv(feedback_file_path, index=False)


def display_knowledge_base(feedback_data):
    if feedback_data.empty:
        st.info("No feedback records available in knowledge base yet.")
    else:
        st.dataframe(feedback_data, use_container_width=True, hide_index=True)


def organize_feedback_sessions():
    st.markdown("### Organize Feedback Sessions")

    session_date = st.date_input("Select Feedback Session Date")
    session_time = st.time_input("Select Feedback Session Time")

    st.subheader("Manage Stakeholders")
    
    if "stakeholders" not in st.session_state:
        st.session_state.stakeholders = get_stakeholder_contact_info()

    st.dataframe(pd.DataFrame(st.session_state.stakeholders), use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        new_stakeholder_name = st.text_input("Name")
    with col2:
        new_stakeholder_position = st.text_input("Position")
    with col3:
        new_stakeholder_email = st.text_input("Email")

    if st.button("Add Stakeholder"):
        if new_stakeholder_name and new_stakeholder_email:
            st.session_state.stakeholders.append({
                "name": new_stakeholder_name,
                "Position": new_stakeholder_position,
                "email": new_stakeholder_email
            })
            st.success(f"Added stakeholder: {new_stakeholder_name}")
            st.rerun()
        else:
            st.warning("Please provide Name and Email.")

    stakeholder_names = [s["name"] for s in st.session_state.stakeholders]
    selected_stakeholders = st.multiselect("Select Stakeholders to Invite", stakeholder_names, default=stakeholder_names)

    if st.button("Send Invitation Mail", type="primary"):
        if not selected_stakeholders:
            st.warning("Please select at least one stakeholder to invite.")
            return

        email_addresses = [
            s["email"] for s in st.session_state.stakeholders if s["name"] in selected_stakeholders
        ]

        send_feedback_session_invitation(session_date, session_time, email_addresses)


def get_stakeholder_contact_info():
    return [
        {"name": "System Admin", "Position": "Technical Lead", "email": "admin@crimenexus.org"},
    ]
