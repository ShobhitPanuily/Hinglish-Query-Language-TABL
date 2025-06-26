# compiler/parser.py
def parse_select(tokens, match, token_index_ref):
    token_index = token_index_ref[0]


    table_name = match("IDENTIFIER")
    match("FROM")  
    match("SELECT")  

    columns = []
    while token_index_ref[0] < len(tokens):
        current_type = tokens[token_index_ref[0]][0]
        if current_type in ("WHERE", "GROUPBY"):
            break
        if current_type == "IDENTIFIER":
            columns.append(match("IDENTIFIER"))
            if token_index_ref[0] < len(tokens) and tokens[token_index_ref[0]][0] == "COMMA":
                match("COMMA")
        else:
            break

    if not columns:
        columns = ["*"]

    where_clause = []
    if token_index_ref[0] < len(tokens) and tokens[token_index_ref[0]][0] == "WHERE":
        match("WHERE")
        while token_index_ref[0] < len(tokens):
            column = match("IDENTIFIER")
            operator = match("OPERATOR")
            value_type, value = tokens[token_index_ref[0]]
            token_index_ref[0] += 1

         
            if value_type == "STRING" and value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value_type == "NUMBER":
                value = int(value)

            where_clause.append((column, operator, value))

            if token_index_ref[0] < len(tokens) and tokens[token_index_ref[0]][0] == "AND":
                match("AND")
            else:
                break

   
    group_by = None
    if token_index_ref[0] < len(tokens) and tokens[token_index_ref[0]][0] == "GROUPBY":
        match("GROUPBY")
        group_by = match("IDENTIFIER")

    
    if token_index_ref[0] < len(tokens):
        raise SyntaxError(f"Unexpected token after valid SELECT: {tokens[token_index_ref[0]]}")

    return {
        "type": "SELECT",
        "table": table_name,
        "columns": columns,
        "where": where_clause,
        "group_by": group_by
    }


def parse_insert(tokens, match, token_index_ref):
    table_name = match("IDENTIFIER")  
    match("INTO")                     
    match("INSERT")                   
    match("VALUES")                   

    values = {}

    while token_index_ref[0] < len(tokens):
        column = match("IDENTIFIER")
        match("OPERATOR")
        value_type, value = tokens[token_index_ref[0]]
        token_index_ref[0] += 1

       
        if value_type == "STRING" and value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        elif value_type == "NUMBER":
            value = int(value)

        values[column.lower()] = value

        if token_index_ref[0] < len(tokens) and tokens[token_index_ref[0]][0] == "AND":
            match("AND")
        else:
            break

  
    if token_index_ref[0] < len(tokens):
        raise SyntaxError(f"Unexpected token after valid INSERT: {tokens[token_index_ref[0]]}")

    return {
        "type": "INSERT",
        "table": table_name,
        "values": values
    }

def parse_join(tokens, match, token_index_ref):
    left_table = match("IDENTIFIER")
    match("JOIN")  # 'jodo'
    right_table = match("IDENTIFIER")
    match("ON")    # 'on'

    left_column = match("IDENTIFIER")
    match("OPERATOR")  # '='
    right_column = match("IDENTIFIER")

    
    if token_index_ref[0] < len(tokens):
        raise SyntaxError(f"Unexpected token after valid JOIN: {tokens[token_index_ref[0]]}")

    return {
        "type": "JOIN",
        "left_table": left_table,
        "right_table": right_table,
        "on": {
            "left_column": left_column,
            "right_column": right_column
        }
    }


def parse_create(tokens, match, token_index_ref):
    def peek(offset=0):
        if token_index_ref[0] + offset < len(tokens):
            return tokens[token_index_ref[0] + offset]
        return ("EOF", "EOF")

    match("CREATE")
    match("TABLE")
    table_name = match("IDENTIFIER")

    columns = []
    if peek()[0] == "LPAREN":
        match("LPAREN")
        while peek()[0] == "IDENTIFIER":
            column_name = match("IDENTIFIER")
            col_type = match("TYPE")
            is_primary = False

            if peek()[0] == "PRIMARY" and peek(1)[0] == "KEY":
                match("PRIMARY")
                match("KEY")
                is_primary = True

            columns.append({
                "name": column_name.lower(),
                "type": col_type,
                "primary": is_primary
            })

            if peek()[0] == "COMMA":
                match("COMMA")
            else:
                break

        match("RPAREN")

    
    if token_index_ref[0] < len(tokens):
        raise SyntaxError(f"Unexpected token after CREATE: {tokens[token_index_ref[0]]}")

    return {
        "type": "CREATE",
        "table": table_name,
        "columns": columns
    }


def parse_delete(tokens, match, token_index_ref):
    def peek(offset=0):
        if token_index_ref[0] + offset < len(tokens):
            return tokens[token_index_ref[0] + offset]
        return ("EOF", "EOF")

    match("DELETE")
    table_name = match("IDENTIFIER")  

    where_clause = []

    if peek()[0] == "WHERE":
        match("WHERE")
        while token_index_ref[0] < len(tokens):
            column = match("IDENTIFIER")
            operator = match("OPERATOR")

            value_type, value = tokens[token_index_ref[0]]
            token_index_ref[0] += 1

         
            if value_type == "STRING" and value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value_type == "NUMBER":
                value = int(value)

            where_clause.append((column, operator, value))

            if peek()[0] == "AND":
                match("AND")
            else:
                break

   
    if token_index_ref[0] < len(tokens):
        raise SyntaxError(f"Unexpected token after DELETE: {tokens[token_index_ref[0]]}")

    return {
        "type": "DELETE",
        "table": table_name,
        "where": where_clause
    }


def parse_update(tokens, match, token_index_ref):
    def peek(offset=0):
        if token_index_ref[0] + offset < len(tokens):
            return tokens[token_index_ref[0] + offset]
        return ("EOF", "EOF")

    match("UPDATE")
    table_name = match("IDENTIFIER")

    match("SET")
    if peek()[0] == "IDENTIFIER" and peek()[1] == "kar":
        match("IDENTIFIER") 

   
    updates = {}
    while token_index_ref[0] < len(tokens):
        column = match("IDENTIFIER")
        match("OPERATOR")
        value_type, value = tokens[token_index_ref[0]]
        token_index_ref[0] += 1

        # Clean value
        if value_type == "STRING" and value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        elif value_type == "NUMBER":
            value = int(value)

        updates[column.lower()] = value

        if peek()[0] == "AND":
            match("AND")
        else:
            break

   
    where_clause = []
    if peek()[0] == "WHERE":
        match("WHERE")
        while token_index_ref[0] < len(tokens):
            column = match("IDENTIFIER")
            operator = match("OPERATOR")
            value_type, value = tokens[token_index_ref[0]]
            token_index_ref[0] += 1

            if value_type == "STRING" and value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value_type == "NUMBER":
                value = int(value)

            where_clause.append((column, operator, value))

            if peek()[0] == "AND":
                match("AND")
            else:
                break

   
    if token_index_ref[0] < len(tokens):
        raise SyntaxError(f"Unexpected token after UPDATE: {tokens[token_index_ref[0]]}")

    return {
        "type": "UPDATE",
        "table": table_name,
        "set": updates,
        "where": where_clause
    }


def parse_loop(tokens, match, token_index_ref):
   
    count_str = match("NUMBER")
    try:
        count = int(count_str)
    except ValueError:
        raise SyntaxError(f"Invalid loop count: {count_str}")

    # Step 2: Match 'BAAR'
    match("BAAR")

   
    if (len(tokens) - token_index_ref[0]) >= 3:
        next_tok = tokens[token_index_ref[0]:token_index_ref[0] + 3]
        if next_tok[0][0] == "IDENTIFIER" and next_tok[1][0] == "INTO" and next_tok[2][0] == "INSERT":
            command = parse_insert(tokens, match, token_index_ref)
        else:
            raise SyntaxError(f"Only INSERT command supported inside loops. Got: {next_tok}")
    else:
        raise SyntaxError("Incomplete command inside loop.")

    
    return {
        "type": "LOOP",
        "count": count,
        "command": command
    }





def parse(tokens):
    if not tokens:
        raise ValueError("No tokens to parse.")

    token_index_ref = [0]

    def match(expected_type):
        if token_index_ref[0] < len(tokens) and tokens[token_index_ref[0]][0] == expected_type:
            token = tokens[token_index_ref[0]]
            token_index_ref[0] += 1
            return token[1]
        else:
            raise SyntaxError(f"Expected {expected_type}, got {tokens[token_index_ref[0]] if token_index_ref[0] < len(tokens) else 'EOF'}")

  
    if len(tokens) >= 3:
        if tokens[1][0] == "FROM" and tokens[2][0] == "SELECT":
            return parse_select(tokens, match, token_index_ref)
        elif tokens[1][0] == "INTO" and tokens[2][0] == "INSERT":
            return parse_insert(tokens, match, token_index_ref)
        elif tokens[1][0] == "JOIN":
            return parse_join(tokens, match, token_index_ref)
 
    command_type = tokens[0][0]

    if command_type == "CREATE":
        return parse_create(tokens, match, token_index_ref)
    elif command_type == "DELETE":
        return parse_delete(tokens, match, token_index_ref)
    elif command_type == "UPDATE":
        return parse_update(tokens, match, token_index_ref)
    elif command_type == "NUMBER" and len(tokens) > 1 and tokens[1][0] == "BAAR":
        return parse_loop(tokens, match, token_index_ref)

    raise SyntaxError(f"Unknown command pattern: {tokens[:3]}")
