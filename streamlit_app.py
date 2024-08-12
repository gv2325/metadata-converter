import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import json

def xml_to_dataframe(xml_data):
    def parse_element(element, parent_path=""):
        # Create a dictionary to hold the parsed data
        parsed_data = {}
        # Iterate over the child elements
        for child in element:
            # Construct the path for the current element
            path = f"{parent_path}/{child.tag}" if parent_path else child.tag
            # If the child has children, recursively parse them
            if list(child):
                parsed_data.update(parse_element(child, path))
            else:
                # If the child has no children, add its text to the dictionary
                parsed_data[path] = child.text
        return parsed_data

    # Parse the XML data
    root = ET.fromstring(xml_data)
    # Parse the root element
    parsed_data = parse_element(root)
    # Convert the parsed data to a DataFrame
    df = pd.DataFrame([parsed_data])
    return df

def main():
    st.title("XML to DataFrame Converter")

    # File uploader
    uploaded_files = st.file_uploader("Upload XML files", type=["xml"], accept_multiple_files=True)

    if uploaded_files:
        all_dfs = []
        for uploaded_file in uploaded_files:
            # Read the uploaded XML file
            xml_data = uploaded_file.read()

            # Convert XML to DataFrame
            df = xml_to_dataframe(xml_data)
            all_dfs.append(df)

        # Concatenate all DataFrames
        final_df = pd.concat(all_dfs, ignore_index=True)

        # Display DataFrame
        st.write("DataFrame:")
        st.dataframe(final_df)

        # Download buttons
        st.download_button(
            label="Download as CSV",
            data=final_df.to_csv(index=False),
            file_name="data.csv",
            mime="text/csv"
        )

        st.download_button(
            label="Download as JSON",
            data=final_df.to_json(orient="records"),
            file_name="data.json",
            mime="application/json"
        )

        st.download_button(
            label="Download as TXT",
            data=final_df.to_csv(index=False, sep='\t'),
            file_name="data.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()