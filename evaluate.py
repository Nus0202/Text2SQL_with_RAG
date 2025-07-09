import json
import os
import text2sql
import prompt_builder
import retrieve
import time
from datetime import datetime, timezone

# path to table.json
base_path = '/Users/shawsun/Desktop/Guelph/DATA6400/Project/Dataset/spider/'
file_name = input("Please enter JSON file name (For example: tables.json): ")
json_file_path = os.path.join(base_path, file_name)

start_time = time.time()

# read json file
with open(json_file_path, 'r', encoding = 'utf-8') as f:
    data = json.load(f)

with open('outputs_with_RAG.txt', 'w', encoding = 'utf-8') as f:
    for i, db in enumerate(data):
        question = db.get('question', 'Unknown')

        retrieved_paragraphs = retrieve.retrieve_schema_paragraphs(question)
        sample_prompt = prompt_builder.construct_prompt(question, retrieved_paragraphs)
        output = text2sql.generate_sql(sample_prompt)

        f.write(f"Output {i + 1}:\n{output}\n")
        if i < len(data) - 1:
            f.write('-' * 50 + '\n\n')
        print(f"Question {i} completed")

# 计算总耗时（三种输出方式）
total_time = time.time() - start_time

# 使用带时区的转换方式
formatted_time = datetime.fromtimestamp(total_time, tz=timezone.utc).strftime('Total duration: %Hh %Mm %Ss')
print(formatted_time)