import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


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

def chat_sum(text):
    chat = ChatOpenAI(temperature=0)
    template = "You are a helpful assistant that summarize the content to around 15% of it's original size. The " \
               "original content is from transcript of lectures, the summarization should be descriptive, instead of " \
               "like speech."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # get a chat completion from the formatted messages
    messages = chat_prompt.format_prompt(text=text).to_messages()
    # print(messages)
    result = chat(messages)
    return result.content


def chat_sum_obs(text):
    chat = ChatOpenAI(temperature=0)
    template = """
Your task is to perform the following actions: 
1 - Summarize the input text with 4 keywords.
2 - Summarize the input text with less than 15 words.
3 - Summarize the input text with keywords of research methods mentioned in the text.

Use the following format:
keywords: <keywords seperated by comma>
summary: <summary>
method: <keywords of research methods seperated by comma>
"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # get a chat completion from the formatted messages
    messages = chat_prompt.format_prompt(text=text).to_messages()
    # print(messages)
    result = chat(messages)
    return result.content


def chat_sum_re(text):
    chat = ChatOpenAI(temperature=0)
    template = """
I want you to extract essential information from the conclusion of a paper. I am going to provide a template for your output . <placeholder> are my placeholders for content. Try to fit the output into one or more of the placeholders that I list. Please preserve the formatting and overall template that I provide. 

This is the template: 

### **What do we know?**
- <Direct Quote>
- <In my own words…>

### **What don’t we know?**
- <Direct Quote>
- <In my own words…>

### **How does the author go about answering that question?**
- <Direct Quote>
- <In my own words…>

### **What do(es) the author(s) find?**
- <Direct Quote>
- <In my own words…>

### **What do we learn from this paper? What is the contribution?**
- <Direct Quote>
- <In my own words…>
"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # get a chat completion from the formatted messages
    messages = chat_prompt.format_prompt(text=text).to_messages()
    # print(messages)
    result = chat(messages)
    return result.content


def prompt_test():
    # Create Text Area Widget to enable user to enter texts
    article_text = st.text_area(":blue[Enter your scientific texts to summarize]")

    # Create Radio Buttons
    # output_size = st.radio(label=":blue[What kind of output do you want?]",
    #                        options=["To-The-Point", "Concise", "Detailed"]
    #                        )

    if st.button("Generate Summary", type='primary'):

        # Use GPT-3 to generate a summary of the article
        res = chat_sum(article_text)
        st.success(res)
        # Give user the option to download result
        st.download_button('Download result', res)
    else:
        st.warning("Not enough words to summarize!")


def sum_obsidian():
    # Create Text Area Widget to enable user to enter texts
    article_text = st.text_area(":blue[Enter your scientific texts to summarize obs]", key="obs")

    # Create Radio Buttons
    # output_size = st.radio(label=":blue[What kind of output do you want?]",
    #                        options=["To-The-Point", "Concise", "Detailed"]
    #                        )

    if st.button("Generate Summary", type='primary', key='obs_key'):

        # Use GPT-3 to generate a summary of the article
        res = chat_sum_obs(article_text)
        st.code(res)
        # Give user the option to download result
        st.download_button('Download result', res)
    else:
        st.warning("Not enough words to summarize!")


def sum_re():
    # Create Text Area Widget to enable user to enter texts
    article_text = st.text_area(":blue[Enter your scientific texts to summarize obs]", key="re")

    # Create Radio Buttons
    # output_size = st.radio(label=":blue[What kind of output do you want?]",
    #                        options=["To-The-Point", "Concise", "Detailed"]
    #                        )

    if st.button("Generate Summary", type='primary', key='re_key'):

        # Use GPT-3 to generate a summary of the article
        res = chat_sum_re(article_text)
        st.code(res)
        # Give user the option to download result
        st.download_button('Download result', res)
    else:
        st.warning("Not enough words to summarize!")


def main():
    page_init()
    prompt_test()
    sum_obsidian()
    sum_re()


if __name__ == "__main__":
    main()
