from .config import API_KEY
import sqlite3
import openai

openai.api_key = API_KEY

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
    
    prompt = f"Create a quiz on the following text: \n{text}\n\n" \
             f"Each question should be in a different line and has 4 possible answers" \
             f"Under the possible answers we should have the correct answer"
    
    res = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = prompt,
        max_token = 3500,
        stop = None,
        temperature = 0.7
    )

    questions = res.choices[0].text

    base_key = ''.join(text.split()[:2])

    index = 1

    while key_exits(cursor, key):
        key = f"{base_key} {index}"
        index += 1

        value = questions
        cursor.execute("INSERT INTO questions (key, values) VALUES (?, ?)", (key, values))
        con.commit()

        return questions



def key_exits(cursor, key):
    cursor.execute("SELECT COUNT(*) FROM questions WHERE key = ?",(key,))
    count = cursor.fetchone()[0]
    return count > 0

def display():
    initialize_database()

    con = sqlite3.connect('questions.db')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()

    return rows