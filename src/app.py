import streamlit as st
import os
from processing import process_file
import tempfile
import pandas as pd
import zipfile
import io

def main():
    st.title("Sentaurus TCAD PLT to CSV")
    
    # File upload for .plt files
    uploaded_files = st.file_uploader("Upload .plt files", type=["plt"], accept_multiple_files=True)
    if uploaded_files:
        if st.button("Process Files"):
            processed_files = []
            with tempfile.TemporaryDirectory() as temp_dir:
                for uploaded_file in uploaded_files:
                    # Process the uploaded file
                    output_csv = process_file(uploaded_file, temp_dir)
                    processed_files.append(output_csv)
                
                # Create a ZIP file containing all processed CSV files
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in processed_files:
                        zipf.write(file_path, os.path.basename(file_path))
                
                # Provide a download button for the ZIP file
                st.download_button(
                    label="Download All as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="processed_files.zip",
                    mime="application/zip"
                )
                
                # Provide a download link for each CSV file with preview
                for output_csv in processed_files:
                    with open(output_csv, "rb") as f:
                        df = pd.read_csv(output_csv)
                        st.write(f"Preview of {os.path.basename(output_csv)}:")
                        st.dataframe(df)
                        st.download_button(
                            label=f"Download {os.path.basename(output_csv)}",
                            data=f,
                            file_name=os.path.basename(output_csv),
                            mime="text/csv"
                        )

if __name__ == "__main__":
    main()