# DataWise

DataWise is an innovative data intelligence tool that empowers users to gain insights into their data effortlessly. Designed for both data analysts and casual users, DataWise transforms natural language queries into MongoDB commands, enabling users to extract valuable information from their datasets.

Key Features:

Natural Language Processing: Users can input their queries in plain language, specifying what they need to know about their data—be it trends, availability, ratings, or other metrics.

Automated Query Generation: Leveraging advanced language models, DataWise converts user queries into optimized MongoDB queries that efficiently extract the required data from the database.

Data Extraction: Once the MongoDB queries are executed, the relevant documents are extracted from the database, providing users with real-time insights.

Insight Generation: A secondary language model processes the extracted documents to generate actionable insights and knowledge, making it easier for users to understand their data without needing deep technical expertise.

User-Friendly Interface: Designed with a focus on usability, DataWise allows users of all backgrounds to interact with their data intuitively and efficiently.

With DataWise, users can unlock the full potential of their data, transforming complex queries into meaningful insights that drive informed decision-making.

# Installation and Setup Instructions
1. Install Dependencies
To install the required dependencies, run the following command:

bash

pip install -r requirements.txt

# 2. MongoDB Setup
Setting Up MongoDB
Set up a MongoDB instance (either local or cloud-based).
Loading Data
Use the provided Python script to load the CSV data file into MongoDB. Run the following command, replacing the placeholders with your actual file path, database name, and collection name:
bash

python load_csv_to_mongo.py --csv path/to/data.csv --db your_db_name --collection your_collection_name

# 3. API Key Configuration for Groc Cloud
Set up your API key for Groc Cloud in the .env file:
bash
GROC_CLOUD_API_KEY=your_api_key

# 4. Run the Application
To launch the application, execute the following command:

bash
streamlit run app.py
# Usage Instructions
Launching the Interface
Access the Streamlit interface, typically at http://localhost:8501.
Query Input
In the input field, type a query in natural language, such as:

"Show me products with prices greater than 50."
"Find items where stock is less than 20."
# Result Generation
The system passes your query to the LLM, which translates it into a MongoDB query.
MongoDB retrieves the requested data.
The LLM processes the data into an insightful summary.
# Viewing Results
The output, including both raw data and summarized insights, appears on the interface.
## Error Handling
Errors are managed at several points in the process:

## Query Generation
Regular expressions validate queries generated by the LLM to ensure they match MongoDB’s syntax.
Queries are structured in both outer and inner JSON formats, accommodating complex queries beyond simple find() operations.
## Database Errors
If MongoDB returns an error (e.g., syntax error, missing collection), the system alerts the user with a friendly error message.
## LLM and API Errors
The system handles Groc Cloud API errors gracefully, including retry logic in case of network issues.
Interface Errors
Errors in the Streamlit interface are logged and shown to the user to avoid confusion.
# Data Management
CSV Data Loading
A Python script, load_csv_to_mongo.py, loads CSV data into MongoDB for easy access.
Each CSV file is parsed and inserted into MongoDB with structured schema handling for fast query response times.
## Data Processing
MongoDB data is extracted into a pandas DataFrame for quick data analysis and manipulation before passing it to the LLM.
## System Security
To ensure secure interaction:

## Limited LLM Access
The LLM does not directly access MongoDB. It only generates queries and analyzes output, ensuring data integrity and security.
## API Security
API keys and sensitive configurations are stored securely in environment variables.
# Performance Optimization
## Efficient Query Handling
Queries are optimized for MongoDB using indexed fields and carefully structured filtering.
The system supports batch processing to minimize memory load when handling large files.
Data Processing Efficiency
DataFrames are processed in memory and cached to reduce redundant API calls, ensuring smoother performance for repeated queries.
Scalability Considerations
Database Scaling
MongoDB's flexible schema and indexing options support scaling for large datasets.
Modular Architecture
The separation of each component (query parsing, LLM processing, MongoDB interaction) allows for independent scaling and easy integration of additional LLMs, APIs, or database engines in the future.

