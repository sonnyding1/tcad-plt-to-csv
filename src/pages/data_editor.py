import streamlit as st
import pandas as pd
import os

def main():
    # mechanism to prevent widgets' keys and values from disappearing on landing a new page
    # see "interrupting the widget cleanup process"
    # https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
    for key in st.session_state.keys():
        st.session_state[key] = st.session_state[key]

    st.title("Edit Data")
    st.write("Edit your processed dataframes here.")

    # Access processed_data from session state
    processed_data = st.session_state.get('processed_data', [])

    if not processed_data:
        st.write("No processed data available. Please upload and process files on the main page.")
        return

    # Allow users to select a file to edit
    filenames = [output["filename"] for output in processed_data]
    selected_filename = st.selectbox("Select a file to edit", filenames)

    # Find the selected dataframe
    selected_data = next((item for item in processed_data if item["filename"] == selected_filename), None)

    if selected_data:
        df = selected_data["df"]

        # Display the dataframe for editing
        edited_df = st.data_editor(df, num_rows="dynamic")

        # Save button
        if st.button("Save Changes"):
            # Update the dataframe in the processed_data list
            selected_data["df"] = edited_df
            st.success(f"Dataframe '{selected_filename}' updated successfully!")

            # Update session state
            st.session_state['processed_data'] = processed_data
    else:
        st.write("Error: Dataframe not found.")

if __name__ == "__main__":
    main()