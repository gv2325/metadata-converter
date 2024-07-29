import streamlit as st
import pandas as pd
import xmltodict
import json

def xml_to_dataframe(xml_data):
    # Convert XML data to a dictionary
    data_dict = xmltodict.parse(xml_data)
    # Convert dictionary to JSON string
    json_data = json.dumps(data_dict)
    # Convert JSON string to pandas DataFrame
    df = pd.json_normalize(json.loads(json_data))
    return df

def main():
    st.title("XML to DataFrame Converter")

    # File uploader
    uploaded_file = st.file_uploader("Upload an XML file", type=["xml"])

    if uploaded_file is not None:
        # Read the uploaded XML file
        xml_data = uploaded_file.read()

        # Convert XML to DataFrame
        df = xml_to_dataframe(xml_data)

        # Display DataFrame
        st.write("DataFrame:")
        st.dataframe(df)

        # Download buttons
        st.download_button(
            label="Download as CSV",
            data=df.to_csv(index=False),
            file_name="data.csv",
            mime="text/csv"
        )

        st.download_button(
            label="Download as JSON",
            data=df.to_json(orient="records"),
            file_name="data.json",
            mime="application/json"
        )

        st.download_button(
            label="Download as TXT",
            data=df.to_csv(index=False, sep='\t'),
            file_name="data.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()