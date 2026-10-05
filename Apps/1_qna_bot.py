from dotenv import load_dotenv
load_dotenv(r"C:\Users\Bhumika\OneDrive\Desktop\GenAI_Series\Notebooks\.env")
import os

print(repr(os.getenv("GOOGLE_API_KEY")))
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.title("🤖AskBuddy - AI QnA Bot")
st.markdown("My QnA Bot with Langchain and Google Gemini!")

query=st.chat_input("Ask Anything ?")
if query:
    print(query)


# que="Who is PM of India ?"
# while True:
    # query=input("User: ")
    # if query.lower() in ["quit", "exit", "bye"]:
        # print("GoodBye 🐱")
        # break
    # res=llm.invoke(query)
    # print("AI: ", res.content, "\n")
