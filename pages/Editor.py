import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.semantic import check_ast, get_database

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="TABL Compiler Editor", layout="wide")

if "command_tables" not in st.session_state:
    st.session_state.command_tables = []

if "output" not in st.session_state:
    st.session_state.output = ""

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"

theme_mode = st.sidebar.radio(
    "Choose Theme",
    ["Light Mode", "Dark Mode"],
    index=1 if st.session_state.theme_mode == "Dark Mode" else 0
)
st.session_state.theme_mode = theme_mode
editor_theme = "chrome" if theme_mode == "Light Mode" else "monokai"

local_css("style_light.css" if theme_mode == "Light Mode" else "style_dark.css")

st.title("TABL Compiler")

editor_col, table_col = st.columns([2, 1])

with editor_col:
    st.subheader("Write Your TABL Commands")

    code = st_ace(
        placeholder="Example:\n"
                    "bana table students (id int primary key, naam varchar, rollno int)\n"
                    "students mein daal value naam = 'Shobhit' aur rollno = 22 aur id = 1\n"
                    "students se nikal",
        language="sql",
        theme=editor_theme,
        height=400,
        font_size=16,
        key="tabl_sql_editor"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Run Commands"):
            st.session_state.output = ""
            st.session_state.command_tables = []

            if code:
                commands = [cmd.strip() for cmd in code.strip().split('\n') if cmd.strip()]
                for i, command in enumerate(commands, 1):
                    try:
                        tokens = tokenize(command)
                        ast = parse(tokens)
                        output = check_ast(ast)

                        if isinstance(output, list) and all(isinstance(row, dict) for row in output):
                            df = pd.DataFrame(output)
                            st.session_state.command_tables.append((i, df))
                            st.session_state.output += f"[Command {i}] Tabular result shown above\n"
                        else:
                            st.session_state.output += f"[Command {i}] {output}\n"

                    except Exception as e:
                        st.session_state.output += f"[Command {i}] Error: {str(e)}\n"

            else:
                st.warning("Please enter some commands.")

    with col2:
        if st.button("Clear Output"):
            st.session_state.output = ""

with table_col:
    st.subheader("Table Viewer")
    db = get_database()

    if not db:
        st.info("No tables created yet.")
    else:
        selected_table = st.selectbox("Select Table", list(db.keys()))
        table = db[selected_table]

        if isinstance(table, dict) and "schema" in table and "rows" in table:
            columns = [col["name"] for col in table["schema"]]
            rows = table["rows"]
            if rows:
                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{selected_table}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("This table has no rows yet.")
        else:
            st.error("Invalid table format.")

st.markdown("---")
st.subheader("Output Log")
if st.session_state.command_tables:
    for idx, df in st.session_state.command_tables:
        st.markdown(f"**Result of Command {idx}:**")
        st.dataframe(df, use_container_width=True, height=min(400, 40 + len(df)*35))
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download Command {idx} Result as CSV",
            data=csv,
            file_name=f"command_{idx}_output.csv",
            mime="text/csv"
        )

st.code(st.session_state.output or "No output yet.", language='text')
