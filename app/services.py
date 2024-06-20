import sqlite3
import replicate
import os

replicate_api_token = os.environ.get('REPLICATE_API', '000')

os.environ['REPLICATE_API_TOKEN'] = replicate_api_token

def initialize_database():
    con = sqlite3.connect('questions.db')
    cursor = con.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                   (id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)''')

    con.commit()
    con.close()

def generate_questions(text):
    initialize_database()

    con = sqlite3.connect('questions.db')
    cursor = con.cursor()

    input_data = {
        "top_p": 1,
        "prompt": f"Create a quiz on the following text: \n{text}\n\n" \
                  f"Each question should be in a different line and has 4 possible answers." \
                  f" Under the possible answers we should have the correct answer.",
        "temperature": 0.75
    }
    
    res = []

    for event in replicate.stream(
        "meta/llama-2-70b",
        input=input_data
    ):
        if hasattr(event, 'text'):
            res.append(event.text)
        
    questions = ''.join(res)

    base_key = ''.join(text.split()[:2])

    index = 1
    key = base_key
    
    while key_exists(cursor, key):
        key = f"{base_key}_{index}"
        index += 1

    cursor.execute("INSERT INTO questions (key, value) VALUES (?, ?)", (key, questions))
    con.commit()

    # Debugging print
    print(f"Inserted Questions: Key={key}, Questions={questions}")

    con.close()

    return questions


def key_exists(cursor, key):
    cursor.execute("SELECT COUNT(*) FROM questions WHERE key = ?", (key,))
    count = cursor.fetchone()[0]
    return count > 0

def display():
    initialize_database()

    con = sqlite3.connect('questions.db')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()

    con.close()
    return rows
