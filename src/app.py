import streamlit as st
import os
from processing import process_file
import tempfile
import pandas as pd
import zipfile
import io

def main():
    st.title("Sentaurus TCAD PLT to CSV")
    
    # Initialize session state for uploaded_files and processed_files
    if 'uploaded_files' not in st.session_state:
        st.session_state['uploaded_files'] = []
    if 'processed_data' not in st.session_state:
        st.session_state['processed_data'] = []
    
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
        
        st.session_state['processed_data'] = processed_data  # Store processed data in session state
    
    # Provide a download button for the ZIP file
    if st.session_state['processed_data']:
        # Create a ZIP file containing all processed CSV files
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item in st.session_state['processed_data']:
                df = item["df"]
                filename = item["filename"]
                csv_data = df.to_csv(index=False)
                zipf.writestr(filename, csv_data)
        
        st.download_button(
            label="Download All as ZIP",
            data=zip_buffer.getvalue(),
            file_name="processed_files.zip",
            mime="application/zip"
        )
        
        # Provide a download link for each CSV file with preview
        for item in st.session_state['processed_data']:
            df = item["df"]
            filename = item["filename"]
            with st.expander(label=filename, expanded=False):
                st.dataframe(df)
                csv_data = df.to_csv(index=False).encode()
                st.download_button(
                    label=f"Download {filename}",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()