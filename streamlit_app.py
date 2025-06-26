import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="TABL Compiler", layout="wide")
local_css("style.css")


with st.sidebar:
    st.markdown("##  TABL Compiler Menu")

    st.markdown("####  Navigation")
    if st.button(" Launch Editor"):
        st.switch_page("pages/Editor.py")

    if st.button(" How It Works"):
        st.switch_page("pages/How_to_Use.py")

    st.markdown("---")
    st.markdown("#### GitHub")
    st.markdown(
        "<div style='text-align:center'>"
        "<a href='https://github.com/ShobhitPanuily/Hinglish-Query-Language-TABL' target='_blank'>"
        "<button class='glow-btn'>View Source Code</button>"
        "</a>"
        "</div>",
        unsafe_allow_html=True
    )


st.markdown("""
<div class="hero-section">
    <h1>Hinglish Query Language - TABL</h1>
    <h2>Translating Annotated Bhasha to Language</h2>
    <p>Create and run Hindi-English SQL queries in your browser. No setup needed — just write, run, and see the result instantly.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="features-section">
    <h2> Key Features</h2>
    <div class="features-grid">
        <div class="feature-box">
            <h3> No Installation</h3>
            <p>Works directly in your browser. No downloads or setups needed.</p>
        </div>
        <div class="feature-box">
            <h3>Hinglish Syntax</h3>
            <p>Write commands like <code>bana table students</code> easily in Hinglish.</p>
        </div>
        <div class="feature-box">
            <h3>Instant Table View</h3>
            <p>Insert data and immediately view it in a beautiful table format.</p>
        </div>
        <div class="feature-box">
            <h3> Multi-Command Support</h3>
            <p>Execute multiple Hinglish queries one after another seamlessly.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
     TABL Compiler | Created by Team Ordino | GEHU Developers 
</div>
""", unsafe_allow_html=True)
