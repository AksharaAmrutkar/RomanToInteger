from xtconfig import config
import sqlite3  # Import sqlite3 for database interactions
import nextpy as xt
import csv
import os
# This code block represents a style dictionary generated using a large language model (LLM). 
# The original prompt for this generation was: "Generate a style dictionary for the following code [paste the code here]".
# Additionally, we have developed the "Nextpy Style Assistant", a tool designed to assist in code styling and best practices. 
# This assistant will be available on our Discord server soon for further support and guidance in code styling.


style = {
    "heading": {
        "text_align": "center",
        "font_size": "36px",
        "line_height": "44px",
        "color": "black",
        "font_family": "DM Sans",
        "max_width": "620px",
        "padding_top": "16px",
        "padding_bottom": "16px",
        "font_weight": "bold",
        "text_shadow": "2px 2px 4px rgba(0, 0, 0, 0.3)"
    },
    "get_started_box": {
        "font_family": "Inter",
        "text_align": "center",
        "font_size": "14px",
        "color": "#222",  
        "background": "#fff",  
        "padding_x": "48px",
        "padding_y": "12px",
        "border_radius": "lg",
        "font_weight": "bold",
        "font_size": "18px",  
        "text_shadow": "1px 1px 2px rgba(0, 0, 0, 0.2)"  
    },
    "vertical_stack_style": {
        "background": "#f5f5f5",  
        "height": "100vh",
        "padding_top": "20%",
        "padding_left": "5%",
        "padding_right": "5%",
        "font_size": "16px",  
    },
    "input_field": {
        "border": "1px solid #ccc",
        "padding": "10px",
        "margin_bottom": "10px",  
    },
    "error_message": {
        "margin_bottom": "10px",  
    }
}

docs_url = "https://nextpy.org/nextpy/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

# Example usage:
db_path = 'C:/Users/HP/Documents/Final_Roman_to_decimal/roman_numerals.db'

# Integrated data-related functions:
def create_table():
    conn = sqlite3.connect("roman_numerals.db")  # Connect to the database
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roman TEXT,
            decimal INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_conversion(roman, decimal):
    conn = sqlite3.connect("roman_numerals.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversions (roman, decimal) VALUES (?, ?)", (roman, decimal))
    conn.commit()
    conn.close()

def get_all_conversions():
    conn = sqlite3.connect("roman_numerals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT roman, decimal FROM conversions")
    data = cursor.fetchall()
    conn.close()
    return data

class State(xt.State):
    roman_number: str = ""
    decimal_number: int = 0
    error_message: str = ""

    ROMAN_VALUES = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }

    def convert_to_decimal(self):
        self.error_message = ""
        decimal = 0
        for i in range(len(self.roman_number)):
            try:
                value = self.ROMAN_VALUES[self.roman_number[i]]
                if i < len(self.roman_number) - 1 and value < self.ROMAN_VALUES[self.roman_number[i + 1]]:
                    decimal -= value
                else:
                    decimal += value
            except KeyError:
                self.error_message = "Invalid Roman numeral entered."
                return

        self.decimal_number = decimal
        if self.error_message == "":
            save_conversion(self.roman_number, self.decimal_number)
        dump_db_to_csv(db_path)  
    def update_roman_number(self, new_value):
        self.roman_number = new_value

def dump_db_to_csv(database_path):
    directory, filename = os.path.split(database_path)
    csv_filename = os.path.join(directory, f"{os.path.splitext(filename)[0]}.csv")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            if tables.index(table) == 0:
                csv_writer.writerow(column_names)

            csv_writer.writerows(data)

    conn.close()



def index():
    heading = xt.text("Roman Numeral Converter", style=style["heading"])
    roman = xt.text("Roman:", color="black")
    roman_input = xt.input(
    value=State.roman_number,
    placeholder="Enter Roman numeral",
    style={"input_field": True},
    on_change=State.update_roman_number  
    )
    decimal_output = xt.text(f"Decimal: {State.decimal_number}")
    error_message = xt.text(State.error_message, color="red")
    convert_button = xt.button("Convert", on_click=State.convert_to_decimal)

    layout = xt.vstack(
        heading,
        roman, 
        roman_input,
        decimal_output,
        error_message,
        convert_button,
        spacing="1em",
        align_items="center",
        justify_content="center",
        height="100vh",
        style={"display": "flex", 
               "align-items": "center",
               "background_color": "#FFB6C1",
                "height": "100vh",
                "font_weight": "bold",
                "text_shadow": "1px 1px 2px rgba(0, 0, 0, 0.2)"  
        },
        
        
    )
    
    return layout


try:
    import sqlite3  
except ImportError:
    print("Please install the sqlite3 module to use this application.")
    exit()

create_table()
app = xt.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&family=Inter&display=swap",
    ],
)
app.add_page(index)



