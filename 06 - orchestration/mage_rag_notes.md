#### SOLVING RAG Pipeline Issues with Mage on GitHub Codespaces

## A. JSON Decode Error : When reading in the documents.json in the ingest block 
Use the URL to the raw file in the github repository and not the direct file link to avoid a JSON decode error . 

## B. Elasticsearch exits unexpectedly :To solve problems in Github Codespaces where elastic search exits unexpectedly , you can change your codespaces configuration 
to the "8 cores 16 GB RAM configuration". This is still free but you may use up your free hours faster. 

## C. Elasticsearch connection refused or Authentication Error: To solve connection refused errors when trying to export te spacy embeddings to elastic search 

    change the connection string to http://<elastic_search_servicename>:9200
    i.e if your docker-compose.yml file runs the elastic search service as : 

    '''  elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
        environment:
        - discovery.type=single-node
        - xpack.security.enabled=false
        ports:
        - "9200:9200"
        - "9300:9300"
        restart: always
        networks:
        - app-network '''

    Your CONNECTION STRING should be `http://elasticsearch:9200`

## D. Exporter block failing in 'ragic' pipeline. 

    i. Go into the edit pipeline for the 'ragic' pipeline 
    ii. Make sure to connect all the blocks in a sequential order to avoid an upstream error 
    i.e Data Loader block ---> Transformer blocks(radiant photon--> vivid nexus-->prismatic axiom) ---> numinous fission
    iii. in the prismatic axion code change the connection string line and save. 
        i.e change connection_string = kwargs.get('connection_string', ''http://localhost:9200'') to connection_string = 'http://elasticsearch:9200'
                    
