import streamlit as st
import pandas as pd

def load_css(path):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="How to Use TABL Compiler", layout="wide")
load_css("style_doc.css")

st.title("TABL Compiler Documentation")
st.markdown("""
Welcome to the **TABL Compiler** documentation. TABL is a Hinglish-based SQL-like language 
that allows you to interact with data using natural, readable commands.
Use this guide to learn how to structure queries, insert records, and analyze data just like in real-life scenarios.
""")

st.markdown("### 1. Create Table")
st.markdown("""
The `bana table` command is used to create a table with a defined schema.
You specify the table name, columns, and optionally set a primary key.

**Real-world Example:**
Imagine creating a record system for your school – you'd want to track student details.

**Complete Working Example:**
```sql
bana table students (id int primary key, naam varchar, rollno int)
```
This command will create a table named `students` with 3 columns:
- `id`: An integer and also the primary key (each student must have a unique ID)
- `naam`: A text column to store student names
- `rollno`: An integer for roll numbers

**Table Structure:**
""")

schema_df = pd.DataFrame({
    "Column": ["id", "naam", "rollno"],
    "Data Type": ["int", "varchar", "int"],
    "Primary Key": ["Yes", "No", "No"]
})
st.table(schema_df)

st.info("Use 'students mein daal value ...' to insert data into this table.")

st.markdown("### 2. Insert Data")
st.markdown("""
Use `mein daal value` to insert records. Each record specifies values for each column.

**Scenario:** Adding new students to the system.

**Complete Working Example:**
```sql
bana table students (id int primary key, naam varchar, rollno int)
students mein daal value id = 1 aur naam = 'Shobhit' aur rollno = 22
students mein daal value id = 2 aur naam = 'Lokesh' aur rollno = 25
```

**Table After Insert:**
""")
insert_df = pd.DataFrame({
    "id": [1, 2],
    "naam": ["Shobhit", "Lokesh"],
    "rollno": [22, 25]
})
st.table(insert_df)

st.markdown("### 3. Select Data (nikal)")
st.markdown("""
Retrieve data using `nikal`.

**Use Cases:**
- Fetching all students
- Getting specific details like names
- Filtering students based on roll number

**Complete Working Example:**
```sql
students se nikal
students se nikal naam, rollno
students se nikal naam jaha rollno = 22
```

**Sample Output:**
""")
select_df = pd.DataFrame({
    "naam": ["Shobhit"],
    "rollno": [22]
})
st.table(select_df)

st.markdown("### 4. Group Data (jodkar)")
st.markdown("""
Use `jodkar` to group records by a column – similar to SQL's GROUP BY.

**Example:**
Group marks of students by subject:
```sql
bana table marks (sid int primary key, subject varchar, marks int)
marks mein daal value sid = 1 aur subject = 'Math' aur marks = 91
marks mein daal value sid = 2 aur subject = 'Math' aur marks = 92
marks mein daal value sid = 3 aur subject = 'English' aur marks = 87
marks se nikal marks jodkar subject
```

**Grouped Output (average marks by subject):**
""")
group_df = pd.DataFrame({
    "subject": ["Math", "English"],
    "marks (avg)": [91.5, 87.0]
})
st.table(group_df)

st.markdown("### 5. Delete Rows (mita)")
st.markdown("""
Use `mita` to remove rows from a table where a condition matches.

**Scenario:** A student left the school – remove their data.

**Complete Working Example:**
```sql
bana table students (id int primary key, naam varchar, rollno int)
students mein daal value id = 1 aur naam = 'Shobhit' aur rollno = 22
students mein daal value id = 2 aur naam = 'Lokesh' aur rollno = 25
mita students jaha naam = 'Shobhit'
```

**After Deletion:**
""")
delete_df = pd.DataFrame({
    "id": [2],
    "naam": ["Lokesh"],
    "rollno": [25]
})
st.table(delete_df)

st.markdown("### ✏️ 6. Update Data (badal)")
st.markdown("""
Use `badal ... set kar` to modify existing entries.

**Use Case:** Correcting a student's roll number.

**Complete Working Example:**
```sql
bana table students (id int primary key, naam varchar, rollno int)
students mein daal value id = 1 aur naam = 'Shobhit' aur rollno = 22
badal students set kar rollno = 35 jaha naam = 'Shobhit'
```

**Updated Table:**
""")
update_df = pd.DataFrame({
    "id": [1],
    "naam": ["Shobhit"],
    "rollno": [35]
})
st.table(update_df)

st.markdown("### 7. Join Tables")
st.markdown("""
Use `jodo` to combine records from two tables using a common column.

**Example:**
Join `students` and `marks` where `id` in students matches `sid` in marks.
```sql
bana table students (id int primary key, naam varchar, rollno int)
bana table marks (sid int primary key, subject varchar, marks int)
students mein daal value id = 1 aur naam = 'Shobhit' aur rollno = 22
students mein daal value id = 2 aur naam = 'Lokesh' aur rollno = 25
marks mein daal value sid = 1 aur subject = 'Math' aur marks = 90
marks mein daal value sid = 2 aur subject = 'Science' aur marks = 88
students jodo marks on id = sid
```
This will combine student names with their subject and marks.

**Joined Table:**
""")
join_df = pd.DataFrame({
    "naam": ["Shobhit", "Lokesh"],
    "rollno": [22, 25],
    "subject": ["Math", "Science"],
    "marks": [90, 88]
})
st.table(join_df)

st.markdown("### 8. Insert in Loops (baar)")
st.markdown("""
Insert same record multiple times using `baar` for testing or dummy data.
However, **primary key rules must be respected**.

**Real-world Example:** Adding multiple items to a grocery bill:
```sql
bana table groceries (item varchar, price int)
groceries mein daal value item = 'Apple' aur price = 50 
groceries mein daal value item = 'Banana' aur price = 40 
3 baar groceries mein daal value item = 'Chips' aur price = 10 
```
**Table After Insertion:**
""")
loop_df = pd.DataFrame({
    "item": ["Apple", "Banana", "Chips", "Chips", "Chips"],
    "price" : [50, 40, 10, 10, 10]
})
st.table(loop_df)

st.markdown("---")
st.info("Ready to try? Switch to the Editor page from the sidebar and copy-paste these examples.")
