
import re

TOKENS = [
    
    ("CREATE", r"\bbana\b"),           
    ("INSERT", r"\bdaal\b"),           
    ("DELETE", r"\bmita\b"),            
    ("UPDATE", r"\bbadal\b"),           
    ("SET", r"\bset\b"),           
    ("SELECT", r"\bnikal\b"),          
    ("FROM", r"\bse\b"),                
    ("INTO", r"\bmein\b"),              
    ("VALUES", r"\bvalue\b"),          
    ("TABLE", r"\btable\b"),            
    ("WHERE", r"\bjaha\b"),           
    ("AND", r"\baur\b"),                

 
    ("JOIN", r"\bjodo\b"),             
    ("ON", r"\bon\b"),                 
    ("GROUPBY", r"\bjodkar\b"),         

    ("BAAR", r"\bbaar\b"),              
    ("NUMBER", r"\b\d+\b"),             

   
    ("OPERATOR", r"=|>=|<=|!=|>|<"),    
    ("COMMA", r","),                    
    ("LPAREN", r"\("),                 
    ("RPAREN", r"\)"),                 


    ("TYPE", r"\bint\b|\bvarchar\b"),  
    ("PRIMARY", r"\bprimary\b"),        
    ("KEY", r"\bkey\b"),                

    ("STRING", r"'[^']*'"),           

    
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    
    ("SKIP", r"[ \t\n]+"),              
    ("MISMATCH", r".")                  
]


def tokenize(code):
    tokens = []
    index = 0

    while index < len(code):
        matched = False
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, index)
            if match:
                value = match.group(0)
                if token_type == "SKIP":
                    pass  # Ignore whitespace
                elif token_type == "MISMATCH":
                    raise SyntaxError(f"Unexpected token: {value}")
                else:
                    tokens.append((token_type, value))
                index = match.end()
                matched = True
                break
        if not matched:
            raise SyntaxError(f"Illegal character at index {index}: {code[index]}")
    return tokens
