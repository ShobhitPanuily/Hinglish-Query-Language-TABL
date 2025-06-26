import os

if __name__ == "__main__":
    port = os.environ.get("PORT", "8501")  
    os.system(f"streamlit run streamlit_app.py --server.port={port} --server.enableCORS=false")
