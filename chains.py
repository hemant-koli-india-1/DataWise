# chains.py
import os
import pandas as pd
from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from datetime import datetime
import re
import utils

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def query_mongodb(self, user_query):
        # LLM prompt for generating MongoDB queries
        prompt = '''
        Generate a MongoDB query based on the user's request: "{user_input}". 
        ### Instructions: 
        - Return only the MongoDB query as a string that can be directly fed into MongoDB. 
        - The output should be syntactically correct for MongoDB operations such as find(), findOne(), aggregate(), etc.
        - Use the following schema for reference:
        | ProductID | ProductName | Category | Price | Rating | ReviewCount | Stock | Discount | Brand | LaunchDate(DD-MM-YYYY) |
        - note that we will be using the query not in javascript but in python so return accordingly and only provide the entire query starting from db.collections.
        in string format 
        Generate a MongoDB query using Python syntax that retrieves documents from a collection. 
        Ensure that you use correct MongoDB operators (prefix with '$') and Python-compatible date handling. 
        For example, use 'datetime.datetime(2022, 1, 1)' instead of 'ISODate'. 
        The query should filter documents where 'LaunchDate' is greater than January 1, 2022, 
        the 'Category' is either 'Home & Kitchen' or 'Sports', 
        and the 'Discount' is greater than or equal to 10, 
        then sort by 'Price' in descending order.
    
        - The output should reflect valid MongoDB query syntax using double ("") and single ('') quotes where necessary.
        - do not provide multiple queries only provide one best and optimum query
        - Return only the MongoDB query as a string that can be directly fed into MongoDB
        - trim the string provide only the query
        - Ensure that all dates are formatted as Python datetime objects using the format: 
          datetime.datetime(year, month, day, hour=0, minute=0, second=0).
        ensure all the above points are followed
        make sure the query has proper format i.e a '$' before gt.gte etc   
        '''
        prompt_template = PromptTemplate(input_variables=["user_input"], template=prompt)
        llm_chain = prompt_template | self.llm
        generated_query = llm_chain.invoke(input={"user_input": user_query})
        mongo_query = generated_query.content.strip('`')
        mongo_query = utils.correct_mongo_query(mongo_query)
        return mongo_query

    def execute_mongodb_query(self, mongo_query):
        # Extract method and arguments from the MongoDB query string

        match = re.search(r'db\.\w+\.(\w+)\((.*)\)', mongo_query)
        if not match:
            raise ValueError("Invalid query format")

        method = match.group(1)
        arguments = match.group(2)
        results = eval(f"self.collection.{method}({arguments})")

        # Convert MongoDB results to a DataFrame
        documents = list(results)
        df = pd.DataFrame(documents)
        return df if not df.empty else None

    def get_insights(self, data, user_query):
        # LLM prompt for generating insights
        prompt = '''
        You are a data analysis assistant with expertise in generating insights from product data. 

        ### User Question:
        {user_input}

        ### Data Overview:
        Here are the details of the products retrieved based on the user's query:

        {df}

        ### Task:
        Based on the user’s question and the provided product data, generate a detailed insight summary. The insights should include:
        1. The total number of products found that meet the criteria.
        2. Key performance insights, including ratings, review counts, and pricing.
        3. Brand performance details, focusing on the brands associated with the products.
        4. A ranking or evaluation of the products based on the criteria given.
        5. Suggestions or next steps for the user based on the findings.
        6.**Format the response using numbered bullet points to differentiate each product and add an extra line space after each product's details.**
        7. leave space between product name and category 
        
        Please ensure that the insights are clear, concise, and easy for the user to understand, avoiding technical jargon. Format your response in a structured manner similar to the example below:

        ### Example Insight Format:
        - **Total Products Found:** X
        - **Product Details:**
        - **Product Name:** [Product1 Name]
        - **Category:** [Product1 Category]
        - **Price:** $[Product1 Price]
        - **Rating:** [Product1 Rating]
        - **Review Count:** [Product1 Review Count]
        - **Brand:** [Product1 Brand]
        - **Launch Date:** [Product1 Launch Date]
        - *(Repeat for each product found)*
  
        - **Key Insights:**
        1. **Overall Performance:** Based on the products found, we have a total of X products that meet your criteria of having a rating below 4.5, more than 200 reviews, and being offered by brands such as Nike or Sony.
        2. **Best Performing Product:** The product with the highest rating among those found is [Best Product Name], with a rating of [Best Product Rating] and [Best Product Review Count] reviews.
        3. **Lowest Performing Product:** Conversely, the product with the lowest rating is [Lowest Product Name], which has a rating of [Lowest Product Rating] and [Lowest Product Review Count] reviews.
        4. **Brand Analysis:** The brand [Most Common Brand] has the most products in this selection, indicating a strong presence in this category.
  
        - **Next Steps:**
        - Consider exploring products with higher ratings for better quality options.
        - If looking for discounts, check if any of these products are currently on sale or promotion.
        - For further details or specific recommendations, feel free to ask!
        '''
        prompt_template = PromptTemplate(input_variables=["df", "user_input"], template=prompt)
        insights_chain = prompt_template | self.llm

        # Prepare input data
        input_data = {
            "df": data.to_string(),
            "user_input": user_query
        }
        generated_insight = insights_chain.invoke(input_data)
        return generated_insight.content
