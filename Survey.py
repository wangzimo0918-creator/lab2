# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

st.write("""
This survey collects information about students' daily habits.

Please enter a category and the number of hours spent on that
activity per day.

Examples:
- Sleep: 7 (7 hours of sleep per day)
- Study: 4 (4 hours of studying per day)
- Exercise: 1 (1 hour of exercise per day)

Please use hours as your unit of measurement.
""")

# DATA INPUT FORM
with st.form("survey_form"):

    category_input = st.text_input(
    "What activity are you reporting? (Sleep, Study, Exercise, etc.)"
)
    
    value_input = st.text_input(
    "How many hours per day do you spend on this activity?"
)

    submitted = st.form_submit_button("Submit Data")

    if submitted:

        # Check that both inputs are filled in
        if category_input.strip() == "" or value_input.strip() == "":
            st.error("Please fill out both fields.")

        else:
            try:
                # Convert value to a number
                value = float(value_input)

                # Create a new row
                new_data = pd.DataFrame({
                    "Category": [category_input.strip()],
                    "Value": [value]
                })

                # Append data to CSV
                if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
                    new_data.to_csv(
                        "data.csv",
                        mode="a",
                        header=False,
                        index=False
                    )
                else:
                    new_data.to_csv("data.csv", index=False)

                st.success("Your data has been submitted!")
                st.write(
                    f"You entered: **Category:** {category_input}, "
                    f"**Value:** {value}"
                )

            except ValueError:
                st.error("Please enter a valid number for the value.")

st.divider()
st.header("Current Data in CSV")

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    current_data_df = pd.read_csv("data.csv")
    st.dataframe(current_data_df)

else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

