################# LIBRARIES #############
import streamlit as st
from summarizer import TransformerSummarizer
from summarizer import Summarizer

from newspaper.api import languages
from google_trans_new import google_translator
from newspaper import fulltext
import requests


## File Processing
import docx2txt
from PyPDF2 import PdfFileReader

################# VARIABLES #############

# The header to simulate a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}

# Languages
languages = (
    "french",
    "english",
    "turkish",
    "arapic",
    "german",
    "spanish",
    "italian",
    "russian",
)
dic = {
    "french": "fr",
    "english": "en",
    "turkish": "tr",
    "arapic": "ar",
    "german": "de",
    "spanish": "es",
    "italian": "it",
    "russian": "ru",
}

summarized_text = ""
translated_text = ""
langue = ""
raw_text = ""

################# FUNCTIONS #############

# File Readers
def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()
    return all_page_text


# Translator
def translatoor(origin, dest):
    translator = google_translator()
    result = translator.translate(origin, lang_tgt=dest)
    return result


# Get the text of a web page
@st.cache
def article_url(url):
    article = fulltext(requests.get(url, headers=headers).text)
    return article


# Summarizer model GPT2
def summary_gpt2(text):
    GPT2_model = TransformerSummarizer(
        transformer_type="GPT2", transformer_model_key="gpt2-medium"
    )
    gpt2_summary = "".join(GPT2_model(text))
    return gpt2_summary


# Summarizer model BERT
def summary_bert(text, num_sentences):
    bert_model = Summarizer()
    bert_summary = "".join(bert_model(text, num_sentences=num_sentences))
    return bert_summary


################# MAIN FUNCTION #############


def main():
    """Text Summarization and Language Translation Web App"""

    global summarized_text
    global translated_text
    global langue
    global raw_text

    st.markdown("<style>h1{color: red;}</style>", unsafe_allow_html=True)
    st.markdown('# <div align="center">TRANSUM</div>', unsafe_allow_html=True)
    st.markdown(
        '## <div align="center">**Summarizer 📃 Translater**</div>',
        unsafe_allow_html=True,
    )
    st.markdown(" ")
    st.markdown(" ")

    st.write("You can listen to music while waiting 🎵")
    music_select = st.selectbox(
        "Select the Song",
        (
            "secret-garden",
            "asli",
            "stromae-papaoutai",
            "ragnbone-human",
            "indila-derniere-danse",
        ),
    )
    audio_file = open("songs/" + music_select + ".mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    st.write("Or just continue without music 😁")

    Which_summarizer = st.selectbox("Summarizer ", ("BERT", "GPT2"))

    if Which_summarizer == "BERT":

        num_sentences = st.number_input(
            "The number of Sentences",
            5,
            100,
            step=1,
            key="num_sentences_ur",
        )

        URL_Text_File = st.selectbox("Url - Text - File ", ("Text", "Url", "File"))

        if URL_Text_File == "File":
            uploaded_file = st.file_uploader(
                "Choose a file", type=["txt", "docx", "pdf"]
            )
            langue = st.selectbox("Select the Language to Translate ", languages)
            if st.button("GO"):
                if uploaded_file is not None:

                    # Check File Type
                    if uploaded_file.type == "text/plain":
                        raw_text = str(uploaded_file.read(), "utf-8")
                    elif uploaded_file.type == "application/pdf":
                        raw_text = read_pdf(uploaded_file)
                    elif (
                        uploaded_file.type
                        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    ):
                        raw_text = docx2txt.process(uploaded_file)

                summarized_text = summary_bert(raw_text, num_sentences)
                translated_text = translatoor(summarized_text, dic[langue])
                ratio = int((1 - len(summarized_text) / len(raw_text)) * 100)
                st.write("Text reduced by {} %".format(ratio))

        if URL_Text_File == "Url":

            # text summarization with BERT
            url = st.text_area("Enter the URL")
            langue = st.selectbox("Select the Language to Translate ", languages)
            if st.button("GO"):
                text_url = article_url(url)
                summarized_text = summary_bert(text_url, num_sentences)
                translated_text = translatoor(summarized_text, dic[langue])
                ratio = int((1 - len(summarized_text) / len(text_url)) * 100)
                st.write("Text reduced by {} %".format(ratio))

        # st.subheader("OR")

        if URL_Text_File == "Text":
            message = st.text_area("Enter the Text", height=250)
            langue = st.selectbox("Select the Language to Translate ", languages)
            if st.button("GO"):
                summarized_text = summary_bert(message, num_sentences)
                translated_text = translatoor(summarized_text, dic[langue])
                ratio = int((1 - len(summarized_text) / len(message)) * 100)
                st.write("Text reduced by {} %".format(ratio))

    if Which_summarizer == "GPT2":

        URL_Text_File = st.selectbox("Url - Text - File ", ("Text", "Url", "File"))

        if URL_Text_File == "File":
            uploaded_file = st.file_uploader(
                "Choose a file", type=["txt", "docx", "pdf"]
            )
            langue = st.selectbox("Select the Language to Translate ", languages)
            if st.button("GO"):
                if uploaded_file is not None:

                    # Check File Type
                    if uploaded_file.type == "text/plain":
                        raw_text = str(uploaded_file.read(), "utf-8")
                    elif uploaded_file.type == "application/pdf":
                        raw_text = read_pdf(uploaded_file)
                    elif (
                        uploaded_file.type
                        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    ):
                        raw_text = docx2txt.process(uploaded_file)

                summarized_text = summary_gpt2(raw_text)
                translated_text = translatoor(summarized_text, dic[langue])
                ratio = int((1 - len(summarized_text) / len(raw_text)) * 100)
                st.write("Text reduced by {} %".format(ratio))

        if URL_Text_File == "Url":
            # text summarization with GPT2
            url = st.text_area("Enter the URL")
            langue = st.selectbox("Select the Language to Translate ", languages)
            if st.button("GO"):
                text_url = article_url(url)
                summarized_text = summary_gpt2(text_url)
                translated_text = translatoor(summarized_text, dic[langue])
                ratio = int((1 - len(summarized_text) / len(text_url)) * 100)
                st.write("Text reduced by {} %".format(ratio))

        # st.subheader("OR")
        if URL_Text_File == "Text":
            message = st.text_area("Paste or Type your Text", height=250)
            langue = st.selectbox("Select the Language to Translate ", languages)
            if st.button("GO"):
                summarized_text = summary_gpt2(message)
                translated_text = translatoor(summarized_text, dic[langue])
                ratio = int((1 - len(summarized_text) / len(message)) * 100)
                st.write("Text reduced by {} %".format(ratio))

    st.success(summarized_text)
    st.write("Translation in", langue, ":")
    st.success(translated_text)


if __name__ == "__main__":
    main()