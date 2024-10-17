# import streamlit as st
# from src.langchain_sql import SQLChain

# chain = SQLChain()
# st.title("T-Shirt Store: Database Q&A")

# quesiton = st.text_input("Ask you question here...")

# if quesiton:
#     response = chain.exec_query(quesiton)
    
#     st.header("Answer")
#     st.write(response)

import streamlit as st
from streamlit_lottie import st_lottie
import requests
from src.langchain_sql import SQLChain

# Function to load Lottie animations from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a Lottie animation
lottie_url = "https://assets4.lottiefiles.com/packages/lf20_0yfsb3a1.json"
lottie_json = load_lottieurl(lottie_url)

# Set page configuration
st.set_page_config(
    page_title="Retail Data Insights",
    page_icon="🛍️",
    layout="wide",
)

# Apply custom CSS styles
st.markdown(
    """
    <style>
    /* Center the main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    /* Style the header */
    .header {
        font-size: 48px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
    }
    /* Style the subheader */
    .subheader {
        font-size: 24px;
        color: #2E86C1;
        text-align: center;
    }
    /* Style the input box */
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 10px;
    }
    /* Style the answer */
    .answer {
        font-size: 20px;
        color: #239B56;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize the SQLChain
chain = SQLChain()

# Create a sidebar
with st.sidebar:
    st.image("resources/mylogo.png")
    st.title("T-Shirt Store")
    st.markdown("## Database Q&A")
    st.markdown("---")
    st.markdown("### Sample Questions")
    st.markdown("- How many total t-shirts are left in stock?")
    st.markdown("- How many t-shirts do we have left for Nike in XS size and white color?")
    st.markdown("- How much is the total price of the inventory for all S-size t-shirts?")
    st.markdown("- How much sales amount will be generated if we sell all small size Adidas shirts today after discounts?")

# Main page content
st.markdown('<div class="header">Retail Data Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Ask questions about your inventory, sales, and discounts data.</div>', unsafe_allow_html=True)

# Display Lottie animation
st_lottie(lottie_json, height=200, key="animation")

# Input area
st.markdown("### Ask your question below:")
question = st.text_input("", placeholder="Type your question here...")

if question:
    with st.spinner("Processing your question..."):
        response = chain.exec_query(question)
        st.markdown('<div class="answer">Answer:</div>', unsafe_allow_html=True)
        st.write(response)
else:
    st.info("Please enter a question to get started.")

# Footer
st.markdown("---")
st.markdown("© 2024 T-Shirt Store - All rights reserved.")

