# main.py
import streamlit as st
from chains import Chain
import mongo_data_setup

mongo_data_setup.setup_database()
# Set up Streamlit UI
st.title("MongoDB Query and Insight Generator")

# Initialize the Chain class
chain = Chain()

# User input text box
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    # Step 1: Generate LLM MongoDB query
    llm_query = chain.query_mongodb(user_input)
    st.subheader("LLM Generated Query")
    st.write(llm_query)

    # Step 2: Query MongoDB using the LLM-generated query
    mongodb_result = chain.execute_mongodb_query(llm_query)
    st.subheader("MongoDB Result")
    st.write(mongodb_result)

    # Step 3: Generate insights based on MongoDB data
    if not mongodb_result.empty:
        insights = chain.get_insights(mongodb_result, user_input)
        st.subheader("Insights from LLM")
        st.markdown(insights, unsafe_allow_html=True)
    else:
        st.write("No data found in MongoDB for the generated query.")
