import json
from openai import OpenAI # type: ignore
import os
import sqlite3
import re
from time import sleep
import numpy as np

# Today's date
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")  # e.g., "2025-09-26"

print("Running db_bot.py!")

# Get directories and open database
fdir = os.path.dirname(__file__)
def get_path(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqlite_db_path = get_path("aidb.sqlite")

# Erase previous database
if os.path.exists(sqlite_db_path):
    os.remove(sqlite_db_path)
    
# Path helpers
fdir = os.path.dirname(__file__)
sql_folder = os.path.join(fdir, "SQL")

sqlite_con = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_con.cursor()

# SQL files
sql_files = [
    "Course.sql",
    "Driver.sql",
    "Player.sql",
    "VehicleBody.sql",
    "VehicleGlider.sql",
    "VehicleTires.sql",
    "Record.sql"
]

schemas = []

for filename in sql_files:
    path = os.path.join(sql_folder, filename)
    with open(path, "r") as f:
        script = f.read()
        
        # Execute the SQL script
        sqlite_cursor.executescript(script)
        print(f"Executed {filename}")
        
        # Extract CREATE TABLE statements for schema
        create_statements = re.findall(r"(CREATE TABLE .*?;)", script, re.IGNORECASE | re.DOTALL)
        schemas.extend(create_statements)

# Combine all table definitions into one string for prompts
combined_schemas = "\n".join(schemas)
print("Combined Schemas:")
print(combined_schemas)

# OPENAI
config_path = get_path("config.json")
print(config_path)
with open(config_path) as config_file:
    config = json.load(config_file)

open_ai_client = OpenAI(api_key = config["openaiKey"])
open_ai_client.models.list() # check if the key is valid (update in config.json)

def get_chat_gpt_response(content):
    stream = open_ai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    response_list = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_list.append(chunk.choices[0].delta.content)

    result = "".join(response_list)
    return result

def run_sql(query):
    try:
        result = sqlite_cursor.execute(query).fetchall()
        return result
    except Exception as e:
        print(f"SQL Error: {e}")
        return None

# strategies
zero_shot_strategy = """
You are an expert at writing SQLite queries.
Here are the tables in the database:

{schemas}

Instructions:
- Only return valid SQLite SELECT statements.
- Do not explain anything.
- Focus only on the tables and columns given.
"""

one_shot_strategy = """
You are an expert at writing SQLite queries.
Here are the tables in the database:

{schemas}

Example:
Question: "Which character has the highest speed?"
SQL: "SELECT CharacterName, Speed_Land = (SELECT MAX(Speed_Land) FROM Driver);"

Instructions:
- Only return valid SQLite SELECT statements for any new question.
- Do not explain anything.
"""

few_shot_strategy = """
You are an expert at writing SQLite queries.
Here are the tables in the database:

{schemas}

Examples:
Question: "Which character has the highest speed?"
-- IMPORTANT: Always select the ID along with the name.
SQL: "SELECT DriverID, CharacterName FROM Driver ORDER BY Speed_Land DESC LIMIT 1;"

Question: "What was the fastest record set on Moo Moo Meadows?"
-- CRITICAL: When querying records, always include Record.Speed (150cc or 200cc).
SQL: "SELECT r.Time, r.Speed, p.PlayerName, d.CharacterName, c.CourseName FROM Record r JOIN Player p ON r.PlayerID = p.PlayerID JOIN Driver d ON r.DriverID = d.DriverID JOIN Course c ON r.CourseID = c.CourseID WHERE c.CourseName = 'Moo Moo Meadows' COLLATE NOCASE ORDER BY r.Time ASC;"

Question: "How many heavy characters are there?"
SQL: "SELECT CharacterName, COUNT(*) FROM Driver WHERE WeightClass = 'Heavy';"

Instructions:
- Only return valid SQLite SELECT statements for any new question.
- Do not explain anything.
- When querying using names (e.g., PlayerName, CharacterName), always use 'COLLATE NOCASE' to ensure case-insensitive matching.
- **ABSOLUTELY ESSENTIAL: Any query that selects record data (Time, Date) MUST select the Record.Speed column.**
- Focus only on the tables and columns given.
"""

sql_query = "SELECT CharacterName FROM Driver ORDER BY Speed_Land DESC LIMIT 1;"
query_results = run_sql(sql_query)

friendly_response_strategy = """
I ran the following SQL query:

{sql_query}

The raw results are:

{query_results}

Please give a concise, friendly answer to the user's original question.
"""

strategies = {
    "zero_shot": zero_shot_strategy.format(schemas=combined_schemas),
    "one_shot": one_shot_strategy.format(schemas=combined_schemas),
    "few_shot": few_shot_strategy.format(schemas=combined_schemas),
    "friendly": friendly_response_strategy
}

def build_lookup_dict(table, id_col, name_col):
    sqlite_cursor.execute(f"SELECT {id_col}, {name_col} FROM {table}")
    return {row[0]: row[1] for row in sqlite_cursor.fetchall()}

def build_all_lookups():
    return {
        "players": build_lookup_dict("Player", "PlayerID", "PlayerName"),
        "courses": build_lookup_dict("Course", "CourseID", "CourseName"),
        "vehicles": build_lookup_dict("VehicleBody", "VehicleBodyID", "VehicleBodyName"),
        "drivers": build_lookup_dict("Driver", "DriverID", "CharacterName"),
        "tires": build_lookup_dict("VehicleTires", "VehicleTireID", "VehicleTireName"),
        "gliders": build_lookup_dict("VehicleGlider", "VehicleGliderID", "VehicleGliderName"),
    }
  
# Build a response that chat can interpret  
def build_friendly_result(query_result, sql_query, lookups, context=None):
    """
    Converts raw SQL query results into human-readable data with stat enrichment.
    Incorporates ID fallbacks (name-to-ID lookup) and conditional stat fetching.
    """
    if not query_result:
        return []

    # Get column names from the last executed query
    columns = [desc[0] for desc in sqlite_cursor.description]
    friendly_result = []

    for r in query_result:
        row_dict = dict(zip(columns, r))
        
        # Potential targets
        id_targets = [
            ("Driver", "DriverID", "CharacterName"),
            ("VehicleBody", "VehicleBodyID", "VehicleBodyName"),
            ("VehicleTires", "VehicleTireID", "VehicleTireName"),
            ("VehicleGlider", "VehicleGliderID", "VehicleGliderName"),
            ("Course", "CourseID", "CourseName"),
            ("Player", "PlayerID", "PlayerName"),
        ]

        # Maintain proper ordering
        for table, id_col, name_col in id_targets:
            id_val = row_dict.get(id_col)
            name_val = row_dict.get(name_col)
            
            # Case 1: We can map using IDs
            if id_val is not None:
                # Allow chat to look up players
                key = table.lower() + "s" if table != "Player" else "players"
                row_dict[table] = lookups[key].get(id_val, f"Unknown {table}")
            
            # Case 2: Use name to find ID to map across
            elif name_val is not None:
                # Perform a single-row lookup to get the missing ID
                sqlite_cursor.execute(f"SELECT {id_col} FROM {table} WHERE {name_col} = ?", (name_val,))
                id_lookup_result = sqlite_cursor.fetchone()
                
                if id_lookup_result:
                    row_dict[id_col] = id_lookup_result[0]
                    # Map the name again, now that the ID is available
                    row_dict[table] = name_val # Name is already known
            
            else:
                row_dict[table] = row_dict.get(name_col, f"N/A {table}")
        
        # Stats dictionary
        row_stats = {
            "Speed": {"Land": 0.0, "Water": 0.0, "AntiG": 0.0, "Glide": 0.0},
            "Handling": {"Land": 0.0, "Water": 0.0, "AntiG": 0.0, "Glide": 0.0},
            "Acceleration": 0.0, "Weight": 0.0, "Traction": 0.0,
            "MiniTurbo": 0.0, "Invincibility": 0.0
        }
        
        # Aggregate speed stats
        speed_land_total = row_dict.get("Total_Speed_Land")

        # Build stats
        if speed_land_total is not None:
            row_stats["Speed"]["Land"] = speed_land_total
            row_stats["Speed"]["Water"] = row_dict.get("Total_Speed_Water", 0.0)
            row_stats["Speed"]["AntiG"] = row_dict.get("Total_Speed_AntiG", 0.0)
            row_stats["Speed"]["Glide"] = row_dict.get("Total_Speed_Glide", 0.0)
            
            row_stats["Handling"]["Land"] = row_dict.get("Total_Handling_Land", 0.0)
            row_stats["Handling"]["Water"] = row_dict.get("Total_Handling_Water", 0.0)
            row_stats["Handling"]["AntiG"] = row_dict.get("Total_Handling_AntiG", 0.0)
            row_stats["Handling"]["Glide"] = row_dict.get("Total_Handling_Glide", 0.0)
            
            row_stats["Acceleration"] = row_dict.get("Total_Acceleration", 0.0)
            row_stats["Weight"] = row_dict.get("Total_WeightValue", 0.0)
            row_stats["Traction"] = row_dict.get("Total_Traction", 0.0)
            row_stats["MiniTurbo"] = row_dict.get("Total_MiniTurbo", 0.0)
            row_stats["Invincibility"] = row_dict.get("Total_Invincibility", 0.0)
        
        # Building from an ID
        elif row_dict.get("DriverID") is not None:
            driver_id = row_dict["DriverID"]
            
            # Execute lookup to get all base stats from the Driver table
            sqlite_cursor.execute("""
                SELECT Speed_Land, Speed_Water, Speed_AntiG, Speed_Glide,
                    Handling_Land, Handling_Water, Handling_AntiG, Handling_Glide,
                    Acceleration, WeightValue, Traction, MiniTurbo, Invincibility
                FROM Driver WHERE DriverID = ?
            """, (driver_id,))
            stats = sqlite_cursor.fetchone()

            if stats:
                (speed_land, speed_water, speed_antig, speed_glide,
                    handling_land, handling_water, handling_antig, handling_glide,
                    acceleration, weight, traction, mini_turbo, invincibility) = stats
                
                row_stats = {
                    "Speed": {"Land": speed_land, "Water": speed_water, "AntiG": speed_antig, "Glide": speed_glide},
                    "Handling": {"Land": handling_land, "Water": handling_water, "AntiG": handling_antig, "Glide": handling_glide},
                    "Acceleration": acceleration, "Weight": weight, "Traction": traction,
                    "MiniTurbo": mini_turbo, "Invincibility": invincibility
                }
        
        row_dict["Stats"] = row_stats

        # Generate the response
        if context and context.get("friendly_summary"):
            summary = (
                f"- **Speed:** Land {row_stats['Speed']['Land']:.2f}, AntiG {row_stats['Speed']['AntiG']:.2f}, "
                f"Water {row_stats['Speed']['Water']:.2f}, Glide {row_stats['Speed']['Glide']:.2f}\n"
                # ... (rest of your summary formatting) ...
            )
            row_dict["friendly_summary"] = summary

        friendly_result.append(row_dict)

    return friendly_result

    
# Example dictionaries
players = {29: "YUTM", 30: "Zae", 27: "Wish"}
courses = {40: "Hyrule Circuit", 41: "Baby Park"}
vehicles = {2: "B-Dasher", 5: "Blue Falcon", 23: "Pipe Frame"}
drivers = {19: "Baby Peach", 9: "Yoshi", 2: "Luigi"}
tires = {9: "Gold Tires", 13: "Monster", 18: "Slim"}
gliders = {1: "Bowser Kite", 7: "Paper Glider", 12: "Plane Glider"}

lookups = build_all_lookups()

# ChatGPT memory log
MAX_MEMORY = 3  # remember the last 3 user messages

# Start with an empty history
conversation_history = [
    {"role": "system", "content": f"The current date today is {today}. Please keep this in mind when answering questions."}
]

# Starter instruction for chat
PREAMBLE = '''
You are an expert at this database for Mario Kart 8 Deluxe.
This database includes tables for:
- Records (world records on tracks)
- Players (who set those records)
- Drivers (characters)
- Courses (tracks)
- VehicleBody, VehicleTire, VehicleGlider (kart parts)

Always:
- Use foreign keys to join IDs with their names (e.g. PlayerID → Player.PlayerName).
- Return names (like "Yoshi" or "Pipe Frame") instead of raw IDs.
- Keep answers concise and friendly, as if explaining to someone who doesn’t know databases.

* When the player queries for a record of any sort, and you return a time, always be sure they know if it is in 150 or 200.
* You can do this by using the Record.Speed column.
* Query both 150 and 200 times if they ask for a track without specifying speed class.
* DO NOT LIMIT 1 if they ask for a world record for a track name and do not specify the speed.

Side notes specific to Mario Kart: Mini Turbo gives you boosts and can be more beneficial than speed.
Invincibility is very useful when playing with other players.

If the user asks about "SNES"/"Super Nintendo", "N64"/"Nintendo 64", "GCN"/"GameCube", "GBA", "Wii", "DS", "3DS", "Wii U", "Tour", "7", "8",
they are referring to the course "Origin" column. So if they include one of those key words, include the origin in their query.
If a track has multiple types with the same name, be sure to list the origin of each one!

If they query for "[Name] Cup" just query the Cup column of Course by "[Name]", as the word cup is not included.
'''

# When the chat wants to know what is bad
worst_prompt = """
When the user asks about the "worst" build, character, kart, tires, or glider:

- Do NOT interpret "worst" as least used.
- Always start by identifying the current "best" (the most frequently used in the Record table).
- Collect the relevant stats for that best option.
- Define "worst" as the option whose stats are furthest from the best option’s stats.
- Use a distance metric (e.g. squared Euclidean distance across Speed, Acceleration, Weight, Handling, Traction, MiniTurbo, Invincibility, etc.).
- Generate SQL that:
  1. Finds the stats of the best option.
  2. Computes the distance between each candidate’s stats and those best stats.
  3. Returns the candidate with the largest distance as the worst.
- Apply this same logic at the appropriate granularity:
  • If the user asks about "worst character," compare drivers.
  • If "worst kart," compare vehicle bodies.
  • If "worst wheels," compare tires.
  • If "worst build," compare full driver + body + tires + glider combos.
"""

# This lets chat remember the last 3 responses
def get_chat_gpt_response_with_memory(user_input, history):
    today = datetime.now().strftime("%Y-%m-%d")
    system_message = {"role": "system", "content": PREAMBLE.format(today=today)}
    messages_to_send = [system_message] + history[-MAX_MEMORY:] + [{"role": "user", "content": user_input}]

    stream = open_ai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages_to_send,
        stream=True
    )

    response_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content

    return response_text

# This lets the user pick their questions rather than using preset questions
def interactive_mode():
    print("Entering interactive mode! Type 'exit' to quit.")

    while True:
        user_question = input("\nAsk a question about your database: ")
        if user_question.lower() in ["exit", "quit"]:
            break

        try:
            # Store user message
            conversation_history.append({"role": "user", "content": user_question})
            history_to_send = conversation_history[-MAX_MEMORY:]

            # Generate SQL
            prompt_for_sql = strategies["few_shot"] + "\n" + user_question # Used few_shot as it's the most relevant

            # Good prompt
            if any(word in user_question.lower() for word in ["best", "good"]):
                prompt_for_sql = """
                When the user asks about the best or a good build, character, or kart:
                - Always query the Record table.
                - Interpret 'best' as the most frequently used build in records.
                - Use COUNT(*) and ORDER BY DESC LIMIT 1.
                """ + prompt_for_sql

            # Bad prompt
            if any(word in user_question.lower() for word in ["bad", "worst"]):
                prompt_for_sql = worst_prompt + prompt_for_sql

            sql_response = get_chat_gpt_response_with_memory(prompt_for_sql, history_to_send)
            sql_response = sanitize_for_sql(sql_response)
            
            # Generate SQL
            print("\nGenerated SQL:")
            print(sql_response)
            sleep(0.25)

            # Run SQL
            query_result = run_sql(sql_response)
            
            # Get column names from cursor
            columns = [desc[0] for desc in sqlite_cursor.description] if sqlite_cursor.description else []
            friendly_result = [dict(zip(columns, row)) for row in query_result] if columns else query_result
            
            print("\nRaw Query Result:")
            print(query_result)
            sleep(0.25)
            
            # Build friendly result using the new helper
            friendly_result = build_friendly_result(query_result, sql_response, lookups)
            print("\nFriendly Result:")
            print(friendly_result)

            # Friendly answer
            friendly_prompt = f"I asked: \"{user_question}\". The SQL query returned: \"{query_result}\". Please give a concise, friendly answer. Interpret the results in a way that even a child could understand."

            friendly_answer = get_chat_gpt_response_with_memory(friendly_prompt, history_to_send)
            print("\nFriendly Answer:")
            print(friendly_answer)
            sleep(0.25)

            # Add assistant response to memory
            conversation_history.append({"role": "assistant", "content": friendly_answer})

        except Exception as e:
            print(f"Error: {e}")
            
# Interpret SQL
def sanitize_for_sql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

if __name__ == "__main__":
    interactive_mode()

sqlite_cursor.close()
sqlite_con.close()
print("Done!")