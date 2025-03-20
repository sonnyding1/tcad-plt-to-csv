import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from processing import process_file

# Default plot size
DEFAULT_PLOT_WIDTH = 10
DEFAULT_PLOT_HEIGHT = 6

def update_x_label():
    st.session_state["x_label"] = st.session_state["x_axis"]

def update_y_label():
    st.session_state["y_label"] = st.session_state["y_axis"]

def main():
    # mechanism to prevent widgets' keys and values from disappearing on landing a new page
    # see "interrupting the widget cleanup process"
    # https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
    for key in st.session_state.keys():
        st.session_state[key] = st.session_state[key]

    st.title("Generate plots from PLT")
    st.write("Or, if you'd like to generate a plot directly from PLT files, please use this page.")

    st.write(st.session_state)

    # a mechanism to declare the keys manually, such that they don't disappear when widgets disappear
    for key in st.session_state.keys():
        st.session_state[key] = st.session_state[key]

    # File upload for .plt files
    uploaded_files = st.file_uploader("Upload .plt files", type=["plt"], accept_multiple_files=True)
    
    if uploaded_files:
        st.session_state['uploaded_files'] = uploaded_files  # Store uploaded files in session state
        
        # Process files immediately upon upload
        st.session_state['processed_data'] = []  # Clear previous processed data
        processed_data = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in st.session_state['uploaded_files']:
                # Process the uploaded file
                output_csv = process_file(uploaded_file, temp_dir)
                
                # Read the CSV data into a DataFrame
                df = pd.read_csv(output_csv)
                
                # Store the DataFrame and filename
                processed_data.append({"filename": os.path.basename(output_csv), "df": df})
            st.session_state['processed_data'] = processed_data
    
    # Access uploaded_files and processed_data from session state
    uploaded_files = st.session_state.get('uploaded_files', [])
    processed_data = st.session_state.get('processed_data', [])
    
    if processed_data:
        # Allow users to select which files to plot
        all_filenames = [output["filename"] for output in processed_data]
        selected_files = st.multiselect("Select files to plot", all_filenames, default=all_filenames, key="selected_files")
        
        # Use an expander to wrap custom labels
        with st.expander("Customize Legend Labels"):
            # Create a dictionary to store custom labels
            custom_labels = {}
            for filename in selected_files:
                custom_labels[filename] = st.text_input(f"Legend label for {filename}:", value=filename, key=f"custom_labels_{filename}")
        
        # Determine available columns
        available_columns = set()
        for output in processed_data:
            if output["filename"] in selected_files:
                available_columns.update(output["df"].columns)
        available_columns = list(available_columns)
        
        # Let users choose x and y axis
        x_axis = st.selectbox("Select X axis", available_columns, key="x_axis", on_change=update_x_label)
        y_axis = st.selectbox("Select Y axis", available_columns, key="y_axis", on_change=update_y_label)

        # Allow users to toggle log scale
        log_scale = st.checkbox("Log scale for Y axis", value=False, key="log_scale")
        
        # Customization options
        with st.expander("Plot Customization"):
            plot_width = st.number_input("Plot Width (inches)", value=DEFAULT_PLOT_WIDTH, key="plot_width")
            plot_height = st.number_input("Plot Height (inches)", value=DEFAULT_PLOT_HEIGHT, key="plot_height")

            # Allow users to customize axis labels and title
            x_label = st.text_input("X axis label", value=x_axis, key="x_label")
            y_label = st.text_input("Y axis label", value=y_axis, key="y_label")
            plot_title = st.text_input("Plot title", value=f"Plot of {x_axis} vs {y_axis}", key="plot_title")
        
        # Create the Matplotlib plot
        fig, ax = plt.subplots(figsize=(plot_width, plot_height))
        
        # Loop through each processed data
        for output in processed_data:
            filename = output["filename"]
            df = output["df"]
            
            # Check if the file is selected for plotting
            if filename in selected_files:
                # Ensure selected columns exist in the DataFrame
                if x_axis in df.columns and y_axis in df.columns:
                    # Plot the data with custom label
                    if log_scale:
                        ax.plot(df[x_axis], abs(df[y_axis]), label=custom_labels[filename])
                    else:
                        ax.plot(df[x_axis], df[y_axis], label=custom_labels[filename])
                    
                else:
                    st.write(f"Required columns ('{x_axis}' and '{y_axis}') not found in {filename}.")
                    st.write(f"Available columns: {df.columns.tolist()}")
        
        # Set the y-axis scale to logarithmic if log_scale is True
        if log_scale:
            ax.set_yscale('log')
            # ax.set_ylim(bottom=1e-12)  # Set a lower limit for the y-axis

        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(plot_title)
        ax.legend()
        ax.grid(True)
        
        # Display the Matplotlib plot in Streamlit
        st.pyplot(fig)
    else:
        st.write("No processed data available. Please upload PLT files first.")

if __name__ == "__main__":
    main()