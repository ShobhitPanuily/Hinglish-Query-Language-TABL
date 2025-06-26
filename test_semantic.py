

from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.semantic import check_ast
import json

commands = [
    "bana table students (id int primary key, naam varchar, rollno int)",
    "students mein daal value naam = 'Shobhit' aur rollno = 22 aur id = 1",
    "students se nikal",
    "students se nikal naam, rollno",
    "students se nikal naam jaha rollno > 20",
    "students se nikal naam, rollno jaha naam = 'Shobhit' aur rollno = 22",
    "mita students jaha rollno = 22",
    "badal students set kar rollno = 25 jaha naam = 'Shobhit'",
    "students jodo marks on id = sid",
    "students se nikal rollno jodkar rollno"
]

for i, cmd in enumerate(commands):
    print(f"\nTest {i+1}: {cmd}")
    try:
       
        tokens = tokenize(cmd)
        print("Tokens:")
        for t in tokens:
            print(" ", t)

    
        ast = parse(tokens)
        print(" Parsed Output:")
        print(json.dumps(ast, indent=2))

      
        result = check_ast(ast)
        print("Semantic Output:")
        print(result)

    except Exception as e:
        print(f"Error: {e}")
