Preparing the ISW-Rag Pipeline 
- Indexing the two FAQ sites using spire.doc 




Containerizing the RAG services using text search and ollama
- Initializing the database - need to change the hostname from postgres to local host and the source port tp 9201
to create a new database , log in using an existing database , like 

pgcli -h localhost  -U your_username -d course_assistant -W

- Generally need to wait for a few minutes after the streamlit application is up . 