import streamlit as st
from openai import OpenAI

if 'result' not in st.session_state:
    st.session_state['result'] = None

if 'file' not in st.session_state:
    st.session_state['file'] = None

if 'file_contents' not in st.session_state:
    st.session_state['file_contents'] = None

def gpt_response(prompt,API_KEY, max_tokens = 256, temperature = 1,frequency_penalty=0,presence_penalty=0):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response.choices[0].message.content

def read_file(uploaded_file): 
    # Code for reading a file here... 
    if uploaded_file is not None: 
        file_contents = uploaded_file.read() 
    text = file_contents.decode("utf-8")
    return text

st.title('GPT Sample App')

with st.sidebar:
    api_key = st.text_input("OpenAI API Key",type="password",value = st.secrets['API_KEY'])
    st.session_state['file'] = st.file_uploader('Upload a file',['txt','pdf'])
    if st.button('Read File'):
        st.session_state['file_contents'] = read_file(st.session_state['file'])


    max_tokens = st.number_input("Max tokens",value = 256)
    temperature = st.number_input("Temperature",min_value=0.0,max_value=2.0,value =1.0,step = .1)
    frequency_penalty = st.number_input('Frequency Penalty',0.0,2.0,0.0,.1)

prompt = st.text_area("Input your prompt",value = st.session_state['file_contents'], height=300)

if st.button('Run prompt',use_container_width=True):
    st.session_state['result'] = gpt_response(prompt,api_key,max_tokens,temperature,frequency_penalty)

if st.session_state['result'] is not None:
    st.subheader('Result:')
    st.markdown(st.session_state['result'])