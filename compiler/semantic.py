

DATABASE = {} 
def check_ast(ast):
    if not isinstance(ast, dict) or "type" not in ast:
        raise ValueError("Invalid AST node")

    command_type = ast["type"]

    if command_type == "CREATE":
        table_name = ast["table"]
        columns = ast.get("columns", [])

        if table_name in DATABASE:
            return f"Error: Table '{table_name}' already exists."

        if not columns:
            return "Error: No columns defined for table."

        primary_keys = [col for col in columns if col.get("primary")]
        if len(primary_keys) > 1:
            return "Error: Only one primary key allowed."

        DATABASE[table_name] = {
            "schema": columns,
            "rows": []
        }

        return f"Table '{table_name}' created with columns: {[col['name'] for col in columns]}"


    elif command_type == "INSERT":
        table_name = ast["table"]
        values = ast["values"]

        if table_name not in DATABASE:
            return f"Error: Table '{table_name}' does not exist."

        schema = DATABASE[table_name]["schema"]
        rows = DATABASE[table_name]["rows"]
        new_row = {}

        for col in schema:
            col_name = col["name"].lower()
            col_type = col["type"]
            is_primary = col.get("primary", False)

            if col_name not in values:
                return f"Error: Missing value for column '{col_name}'."

            val = values[col_name]

         
            try:
                if col_type == "int":
                    val = int(val)
                elif col_type == "varchar":
                    val = str(val)
            except Exception:
                return f"Error: Column '{col_name}' must be of type {col_type}."

            # Primary key check
            if is_primary:
                for row in rows:
                    if row.get(col_name) == val:
                        return f"Error: Duplicate value for primary key '{col_name}'."

            new_row[col_name] = val

        rows.append(new_row)
        return f"Row inserted into table '{table_name}'."

    elif command_type == "SELECT":
        table_name = ast["table"]
        columns = ast.get("columns", ["*"])
        where_clause = ast.get("where", [])
        group_by = ast.get("group_by")  


        if table_name not in DATABASE:
            return f"Error: Table '{table_name}' does not exist."

        data = DATABASE[table_name]["rows"]
        filtered = []

        for row in data:
            match = True
            for col, op, val in where_clause:
                if col not in row:
                    match = False
                    break

                row_val = row[col]
                try:
                    if isinstance(row_val, int):
                        val = int(val)
                    elif isinstance(row_val, str):
                        val = val.strip("'")
                except:
                    match = False
                    break

                if op == "=" and row_val != val:
                    match = False
                elif op == "!=" and row_val == val:
                    match = False
                elif op == ">" and row_val <= val:
                    match = False
                elif op == "<" and row_val >= val:
                    match = False
                elif op == ">=" and row_val < val:
                    match = False
                elif op == "<=" and row_val > val:
                    match = False

            if match:
                filtered.append(row)
      
        if group_by:
            grouped = {}
            for row in filtered:
                key = row.get(group_by)
                if key not in grouped:
                    grouped[key] = {col: row[col] for col in columns if col in row}
            return list(grouped.values())


        if columns == ["*"]:
            return filtered
        else:
            return [{col: row[col] for col in columns if col in row} for row in filtered]
    
    elif command_type == "DELETE":
        table_name = ast["table"]
        where_clause = ast.get("where", [])

        if table_name not in DATABASE:
            return f"Error: Table '{table_name}' does not exist."

        rows = DATABASE[table_name]["rows"]
        original_count = len(rows)

        def row_matches(row):
            for col, op, val in where_clause:
                if col not in row:
                    return False
                row_val = row[col]

               
                try:
                    if isinstance(row_val, int):
                        val = int(val)
                    elif isinstance(row_val, str):
                        val = val.strip("'")
                except:
                    return False

              
                if op == "=" and row_val != val:
                    return False
                elif op == "!=" and row_val == val:
                    return False
                elif op == ">" and row_val <= val:
                    return False
                elif op == "<" and row_val >= val:
                    return False
                elif op == ">=" and row_val < val:
                    return False
                elif op == "<=" and row_val > val:
                    return False
            return True

       
        DATABASE[table_name]["rows"] = [row for row in rows if not row_matches(row)]
        deleted_count = original_count - len(DATABASE[table_name]["rows"])

        return f"Deleted {deleted_count} row(s) from '{table_name}'."
    
    elif command_type == "UPDATE":
        table_name = ast["table"]
        updates = ast["set"]
        where_clause = ast.get("where", [])

        if table_name not in DATABASE:
            return f"Error: Table '{table_name}' does not exist."

        rows = DATABASE[table_name]["rows"]
        update_count = 0

        for row in rows:
            match = True
            for col, op, val in where_clause:
                if col not in row:
                    match = False
                    break
                row_val = row[col]
                if op == "=" and row_val != val:
                    match = False
                elif op == "!=" and row_val == val:
                    match = False
                elif op == ">" and row_val <= val:
                    match = False
                elif op == "<" and row_val >= val:
                    match = False
                elif op == ">=" and row_val < val:
                    match = False
                elif op == "<=" and row_val > val:
                    match = False

            if match:
                for col, val in updates.items():
                    row[col] = val
                update_count += 1

        return f" Updated {update_count} row(s) in '{table_name}'."

    elif command_type == "JOIN":
        left = ast["left_table"]
        right = ast["right_table"]
        on = ast["on"]

        if left not in DATABASE or right not in DATABASE:
            return f"Error: One or both tables ('{left}', '{right}') do not exist."

        left_rows = DATABASE[left]["rows"]
        right_rows = DATABASE[right]["rows"]
        joined = []

        for lrow in left_rows:
            for rrow in right_rows:
                if lrow.get(on["left_column"]) == rrow.get(on["right_column"]):
                    joined.append({**lrow, **rrow})

        return joined

    elif command_type == "LOOP":
        count = ast["count"]
        command = ast["command"]
        results = []

        for _ in range(count):
            result = check_ast(command)
            results.append(result)

        return f"Loop executed {count} times:\n" + "\n".join(str(r) for r in results)



    else:
        return f"Error: Unknown command type '{command_type}'."

def get_database():
    return DATABASE
