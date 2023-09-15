from distutils.log import error
from unittest import result
from numpy import append
import nltk
import streamlit as st
from collections_parser import File
from searchEngine import main, query_expansion_with_feedback
import copy

Paths = {'CRAN': './collections/cran.all.1400',
    'CISI': './collections/CISI.ALL'}

# Text/title
st.title("Search Engine")


# self.indexNumber: int = None
# self.title: str = ''
# self.author: str = ''
# self.info: str = ''
# self.work: str = ''
# self.frequency: dict[str:int]= {}
# self.normalizeFrequency : dict[str:int] = {}
# self.maxFrequency : int= 0
# self.weight: dict[str:int] = {} 

def Feedback(_index):
    
    try:
        result = query_expansion_with_feedback( st.session_state['documents_list'], st.session_state['retrieved_data'][0][_index])
        
        st.session_state['retrieved_data'] = result
        st.session_state['expanded'] = True
    except:
        st.error('Something went wrong while expanding')
        st.session_state['retrieved_data'] = []
        st.session_state['expanded'] = False
    


# Show data about a file.
def fileCard(file: File, index):
    col1, col2 = st.columns([1, 4])
    
    col1.write(file.indexNumber)  #aqui hubo un error :'list 'object has no attribute 'indexNumber'
    if not st.session_state['expanded']:
        col2.button('relevant', key=index, on_click=Feedback, kwargs={'_index': index})
    if file.title != '':
        st.subheader("Title:")
        st.text(file.title)
    
    if file.author != '':
        st.subheader("Author:")
        st.text(file.author)

    if file.work != '':
        st.subheader("Content:")
        if len(file.work) > 120:
            st.text(file.work[:120] + '...')
        else:
            st.text(file.work)

    if file.info != '':
        st.subheader("Information:")
        st.text(file.info)
    
    st.markdown("""---""")


# Calls search engine to run a query.
def Search(query):
    st.session_state['retrieved_data'] = []
    st.session_state['expanded'] = False
    if query == '':
        st.warning('Please write a query.')
        return
    try:
        rank_list, documents_list, documents_term, result = main(Paths[st.session_state['selected_collection']],
            None, None, query=query)
        st.session_state['retrieved_data'] = result
        st.session_state['rank_list'] = rank_list
        st.session_state['documents_list'] = documents_list
        st.session_state['documents_term'] = documents_term
        st.session_state['query'] = query
    except:
        st.error('Something went wrong. Please contact the support team!!')
        

def App():
    st.session_state['selected_collection'] = st.sidebar.selectbox(
        "Please, choose a collection.",
        [*Paths.keys()]
    )
    if st.session_state['single_query']:
        # Main view: To write the queries and select the Collection.
        st.write("Querie a collection.")
        currentQuery = st.text_input(
            'Searcher',
            max_chars=200,
            placeholder='Write your query here.',
            key='query_input'
        )
        st.button('Search', key='searchBtn',# disabled=st.session_state['query'] == currentQuery,
            on_click=Search, kwargs={'query': currentQuery})
        if len(st.session_state['retrieved_data']) > 0 :
            st.header('Results:')
            
            for item in st.session_state['retrieved_data']:
                _index = 0
                for file in item:
                    fileCard(file, _index)
                    _index += 1
    else:
        # Data view: To show the retrieved data from file queries.
        st.write("see the data")
    

if __name__ == '__main__':
    if 'single_query' not in st.session_state:
        st.session_state['single_query'] = True
    
    if 'query' not in st.session_state:
        st.session_state['query'] = ''
    
    if 'retrieved_data' not in st.session_state:
        st.session_state['retrieved_data'] = []

    if 'rank_list' not in st.session_state:
        st.session_state['rank_list'] = None
    
    if 'documents_list' not in st.session_state:
        st.session_state['documents_list'] = None

    if 'documents_term' not in st.session_state:
        st.session_state['documents_term'] = None
    
    if 'expanded' not in st.session_state:
        st.session_state['expanded'] = False

    if 'selected_collection' not in st.session_state:
        st.session_state['selected_collection'] = ''
    
    App()

    