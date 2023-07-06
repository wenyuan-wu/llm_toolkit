import streamlit as st


print(st.secrets["gcp_service_account"]["client_email"])


def test_func(text):
    hard_coded_text = """So this is long paragraph which contains multiple lines \
    without line breaks."""
    return hard_coded_text


print(test_func("test"))

another_text = """
Your task is to perform the following actions: 
1 - Summarize the following text delimited by <> with 4 keywords.
2 - Summarize the following text delimited by <> with 1 sentence.
3 - Summarize the following text delimited by <> with keywords of research methods mentioned in the text.

Use the following format:
text: <text to summarize>
keywords: <keywords seperated by comma>
summary: <summary>
method: <keywords of research methods seperated by comma>

Text: <{text}>
"""

print(another_text)


another_text = """
Your task is to perform the following actions: 
1 - Summarize the input text with 4 keywords.
2 - Summarize the input text with 1 sentence.
3 - Summarize the input text with keywords of research methods mentioned in the text.

Use the following format:
keywords: <keywords seperated by comma>
summary: <summary>
method: <keywords of research methods seperated by comma>
"""