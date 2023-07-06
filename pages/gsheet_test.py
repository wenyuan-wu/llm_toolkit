import streamlit as st
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import pandas as pd


def page_init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
    # setup streamlit page
    st.set_page_config(
        page_title="Prompt Engineering Playground",
        page_icon="🤖"
    )
    st.write("# Prompt Engineering Playground 🤖")
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
    """
    )


def main():
    page_init()
    # prompt_test()
    # sum_obsidian()
    # gsheet_test()
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    conn = connect(
        ":memory:",
        adapter_kwargs={
            "gsheetsapi": {
                "service_account_file": ".streamlit/gc_cred.json",
                # "service_account_info": {
                #     "type": "service_account",
                #     ...
                # },
                "subject": st.secrets["gcp_service_account"]["client_email"],
            },
        },
    )

    # Perform SQL query on the Google Sheet.
    # Uses st.cache_data to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def run_query(query):
        rows = conn.execute(query)
        rows = rows.fetchall()
        return rows

    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')
    col_names = ["id", "type", "language", "prompt_sum", "variable", "prompt_text"]
    df = pd.DataFrame(rows, columns=col_names)
    st.dataframe(df)
    # Print results.
    for row in rows:
        st.write(row[0])
        st.write(row[-1])
        # st.write(f"{row.id} has a :{row.prompt_text}:")


if __name__ == "__main__":
    main()
