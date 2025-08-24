import streamlit as st
from deep_translator import GoogleTranslator

##Title pass
st.set_page_config(page_title="Language Translator",layout = 'centered')
st.title("Language Translator")

###Input
text=st.text_area("Enter your text",height=120)
languages=GoogleTranslator.get_supported_languages(as_dict=True)
#logic
lang_name= [lang.title() for lang in languages.values()]
lang_code= {lang.title() :code for code,lang in languages.items()}

default_s=lang_name.index("English") if "English" in lang_name else 0
default_t=lang_name.index("Hindi") if "Hindi" in lang_name else 1
col1,col2=st.columns(2)
with col1:
    s=st.selectbox("Source lang",lang_name,index=default_s)
with col2:
    t=st.selectbox("Target Lang",lang_name,index=default_t)

if st.button("Translate"):
    if text.strip():
        try:
            translated_text=GoogleTranslator(source=lang_code[s],
                                            target=lang_code[t]).translate(text)
            st.success("Translated Text")
            st.text_area("Output",translated_text,height=120)
        except Exception as e:
            print("Translation failed !!!",e)
    else:
        st.warning("Please enter text to translate!!!")
