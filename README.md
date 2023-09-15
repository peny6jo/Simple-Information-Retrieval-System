# Simple-Information-Retrieval-System
"The problem of Information Retrieval can be summarized simply as 'given an information need (query + user profile + ... ) and a set of documents, order the documents from most to least relevant to that need and present a subset of the most relevant ones.'"

This work is part of the consolidation of the content learned in the subject  Information Retrieval Systems. We expose the model chosen for the  development of the search engine, the vector model, the design and implementation of the code of this model is explained, testing it with at least two collections. In addition, the evaluation metrics of this system are explained,as well as the results obtained when developing them with the different collections and an idea is presented to carry out query expansion through the K-Means grouping algorithm (for which we rely also in the use of the Elbow Method) and with user feedback support. The advantages and disadvantages of the model used are also proposed, as well as recommendations for future work.

Python as programming language.

Numpy, NLTK and SKLearn modules that provide tools for working with collections and processing data.  

Math module to work with mathematical functions and matPlotLib to graph.  

Streamlit framework, for the deployment of the web application necessary.

Run the project:

Create the virtual environment and install dependencis using command <pipenv shell>

Once inside the environment go to the address where the app.py file is located and use the command <streamlit run app.py>
