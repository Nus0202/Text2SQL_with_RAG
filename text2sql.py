import prompt_builder
import retrieve
from ollama import chat
import re

def generate_sql(prompt):
    response = chat(
        model="deepseek-r1:8b",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    answer = response['message']['content']
    clean_answer = re.sub(r'<think>.*?</think>', '', answer, flags = re.DOTALL).strip()
    return clean_answer

# main function
if __name__ == "__main__":
    user_query = input("Please enter your question: ")
    retrieved_paragraphs = retrieve.retrieve_schema_paragraphs(user_query)
    sample_prompt = prompt_builder.construct_prompt(user_query, retrieved_paragraphs)
    sql_query = generate_sql(sample_prompt)
    print("Generated SQL:\n", sql_query)
    print("Retrieved Paragraphs:\n", retrieved_paragraphs)