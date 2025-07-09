import json
import os

# path to table.json
base_path = '/Users/shawsun/Desktop/Guelph/DATA6400/Project/Dataset/spider/'
file_name = input("Please enter JSON file name (For example: tables.json): ")
json_file_path = os.path.join(base_path, file_name)

# read json file
with open(json_file_path, 'r', encoding = 'utf-8') as f:
    data = json.load(f)

final_md = ""

# read schema from data
for db in data:
    db_id = db.get("db_id", "Unknown")
    tables = db.get("table_names_original", [])
    col_names = db.get("column_names_original", [])
    col_types = db.get("column_types", [])
    primary_keys = db.get("primary_keys", [])
    foreign_keys = db.get("foreign_keys", [])
    column_details = {}

    for i, col in enumerate(col_names):
        table_index, col_name = col
        if table_index == -1:
            continue

        table_name = tables[table_index]
        col_type = col_types[i]

        pk_flag = " [PK]" if i in primary_keys else ""
        fk_flag = ""
        for fk in foreign_keys:
            source_index, target_index = fk
            if i == source_index:
                target_table_index, target_col_name = col_names[target_index]
                target_table = tables[target_table_index]
                fk_flag = f" [FK -> {target_table}.{target_col_name}]"
                break
        col_info = f"{col_name}: {col_type}{pk_flag}{fk_flag}"

        if table_name not in column_details:
            column_details[table_name] = []
        column_details[table_name].append(col_info)

    # Output Markdown
    md_output = f"## Database: {db_id}\n\n"
    for table, cols in column_details.items():
        md_output += f"### Table: {table}\n"
        for col in cols:
            md_output += f"- {col}\n"
        md_output += "\n"
    md_output += "-" * 40 + "\n\n"
    
    # Add Markdown to final_md
    final_md += md_output

# Write Markdown to extracted_schema.md
output_file = input("Please enter the output file name (For example: extracted_schema.md): ")
with open(output_file, "w", encoding="utf-8") as f_out:
    f_out.write(final_md)
print(f"Schema information saved to {output_file}")