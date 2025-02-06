# Importing Dependencies
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.chains.combine_documents import create_stuff_documents_chain

from .prompts import summary_prompt, emotion_prompt, character_prompt

import warnings
warnings.filterwarnings("ignore")

# Load the environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY=os.getenv("SERPER_API_KEY")

def summarize_text(text):
    """
    Summarizes the text using the OpenAI API.
    """
    # Initialize LLM
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)
    
    # Define the system prompt and human message
    messages = [
        SystemMessage(summary_prompt),
        HumanMessage(text)
    ]
    
    # Get the summary
    summary = llm.invoke(messages)
    return summary.content

def detect_emotion(text):
    """
    Detects the emotion in the text using the OpenAI API.
    """
    # Initialize LLM
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)
    
    # Define the system prompt
    messages = [
        SystemMessage(emotion_prompt),
        HumanMessage(text)
    ]
    
    # Get the emotion
    emotion = llm.invoke(messages)
    return emotion.content

def search_book(text):
    """
    Searches for the book containing the text using the SerpAPI.
    """
    # Initialize the Google Serper API Wrapper
    search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
    
    # Search the web and get the results
    urls = []
    results = search.results(text)

    for i in results["organic"][:2]:
        urls.append(i['link'])

    # Initialize the WebBaseLoader
    loader = WebBaseLoader(urls)
    docs = loader.load()

    # Initialize LLM
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)

    # Prompt for the chain
    prompt = ChatPromptTemplate.from_template("Write only the possible name of the book and the author of the passage from the following documents: {context}")

    # Create the chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Run the chain
    result = chain.invoke({"context": docs})
    return result

def count_words(text):
    """
    Counts the number of words in the text.
    """
    return len(text.split())

def detect_character(text):
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)
    
    messages = [
        SystemMessage(content=character_prompt),
        HumanMessage(content=text)
    ]

    response = llm.invoke(messages)
    return response.content