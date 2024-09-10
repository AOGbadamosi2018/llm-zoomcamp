# llm-zoomcamp

This codespaces progresses the learnings from the monitoring stage. 

It employs Mage for orchestration. 



### PROJECT - BUILDING A QUICKTELLER FAQ 

Converted Quickteller html page to docx 
Uploaded the document to publicly available google drive.
Indexing the Document for easy retreival. 
Connected elastic search service for storing the index and cosine similarity for text search. 
Used Hugging Face's Sentence Embeddings encode the text. 
Provided Context to gpt's -40 mini
Computed the cost per interaction. 

---> Obtained second document , trying to iterate. 


#### HOW TO RUN 
Create a virtual environmentt 
Install all the dependencies in the requirements.txt file in the 01-intro/project_isw folder 
Export OPENAI_API_KEY to the environment 
CHECK OPENAI_API_KEY is recognized by the environment by using echo $OPENAI_API_KEY
Start the elastic service - (Need to host on a server so it's always available.)
Run the Operationalized Rag Flow. 

[ X ] - Orchestration(Index Update) with Mage 
[ X ] - Deployment with FLASK ? 
[ X ]- Monitoring with Grafana. 