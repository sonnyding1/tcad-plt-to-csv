# TCAD PLT to CSV

This project is a Streamlit web application that allows users to upload `.plt` files from Sentaurus TCAD, and receive a converted CSV file. It's live on streamlit: [https://tcad-plt2csv.streamlit.app/](https://tcad-plt2csv.streamlit.app/)

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/sonnyding1/tcad-plt2csv.git
cd tcad-plt2csv
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage

To run the Streamlit web application, execute the following command:

```bash
streamlit run src/app.py
```

Once the application is running, you can upload `.plt` files. The application will process the files and provide you with the corresponding CSV outputs.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## Acknowledgements

- [Pytaurus](https://github.com/thomashirtz/pytaurus/) for the `.plt` file parsing logic.
- [Streamlit](https://streamlit.io/) for the web application framework.
