import flet as ft
import sqlite3
import requests
import random

# --- DATA ---
emotions_bad = [("😢", "Sad"), ("😠", "Angry"), ("😰", "Stressed"), ("😞", "Overwhelmed"), ("🥱", "Tired")]
emotions_Notgood = [("😴", "Unmotivated"), ("😔", "Insecure"), ("😒", "Annoyed"), ("😅", "Disappointed"), ("🙃", "Bored")]
emotions_neutral = [("🙂", "Okay"), ("😌", "Calm"), ("🤔", "Thoughtful"), ("😀", "Fine"), ("😐", "Unbothered")]
emotions_Good = [("😁", "Happy"), ("🫡", "Motivated"), ("☺️", "Proud"), ("🫨", "Energized"), ("😇", "Peaceful")]
emotions_Great = [("🤩", "Excited"), ("🥳", "Joyful"), ("🥰", "Loved"), ("😜", "Passionate"), ("☺️", "Inspired")]

reasons = [("💼", "Work"), ("👯", "Friends"), ("👨‍👩‍👧", "Family"), ("📚", "School"), ("💭", "Personal")]

def database():
    conn = sqlite3.connect("moods.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT,
            reason TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP)
            """)
    conn.commit()
    conn.close()

# --- IMPROVED API LOGIC ---
def get_song(mood):
    try:
        # We search for 'mood + music' and look at the top 50 results for variety
        url = f"https://itunes.apple.com/search?term={mood}+music&limit=50&entity=song"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data["resultCount"] > 0:
            # Pick a random song from the results found
            random_song = random.choice(data["results"])
            song_name = random_song["trackName"]
            artist = random_song["artistName"]
            return f"{song_name} by {artist}"
    except:
        pass
    
    # Fallback list if the API fails or finds nothing
    backups = ["Keep On Pushing by The Impressions", "Lovely Day by Bill Withers", "Don't Stop Me Now by Queen"]
    return random.choice(backups)

def main(page: ft.Page):
    page.title = "Mood Tracker"
    page.window_width = 400
    page.window_height = 700
    page.bgcolor = "#ffd6e7"
    database()

    def show_moods(e):
        page.controls.clear()
        
        # Helper to make containers
        def mood_box(img, emo_list, label):
            return ft.Container(
                content=ft.Image(src=f"images/{img}.PNG", width=150, height=150),
                on_click=lambda _: survey(page, emo_list, label, show_moods)
            )

        row = ft.Row(
            scroll="auto",
            controls=[
                mood_box("Bad", emotions_bad, "Bad"),
                mood_box("Notgood", emotions_Notgood, "Not Good"),
                mood_box("neutral", emotions_neutral, "Neutral"),
                mood_box("Good", emotions_Good, "Good"),
                mood_box("Great", emotions_Great, "Great"),
            ]
        )

        page.add(
            ft.Column([
                ft.Text("Select your mood", size=30, color="#ff4f87", weight="bold"), 
                row
            ], horizontal_alignment="center")
        )
        page.update()

    # Welcome Screen
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Mood Tracker", size=40, weight="bold", color="#ff4f87"),
                ft.Text("How are you feeling today?", size=18, color="#444444"),
                ft.ElevatedButton("Start", bgcolor="#ff8fb1", color="white", width=150, on_click=show_moods)
            ], alignment="center", horizontal_alignment="center", spacing=30),
            expand=True
        )
    )
    page.update()

def survey(page, emotion_list, label, go_back):
    page.controls.clear()
    page.add(ft.TextButton("Back", style=ft.ButtonStyle(color="#ff4f87"), on_click=lambda _: go_back(None)))
    page.add(ft.Text("What is your specific feeling?", size=20, color="#ff4f87", weight="bold"))

    rows = []
    for emoji, name in emotion_list:
        rows.append(ft.Column([
            ft.IconButton(content=ft.Text(emoji, size=40), 
                          on_click=lambda e, n=name: show_reasons(page, n, go_back)),
            ft.Text(name, size=12, color="#ff4f87")
        ], horizontal_alignment="center"))
        
    page.add(ft.Row(controls=rows, alignment="center", wrap=True))
    page.update()

def show_reasons(page, selected_emotion, go_back):
    page.controls.clear()
    page.add(ft.TextButton("Back", style=ft.ButtonStyle(color="#ff4f87"), on_click=lambda _: go_back(None)))
    page.add(ft.Text(f"Why do you feel {selected_emotion}?", size=20, color="#ff4f87", weight="bold"))

    def save_and_recommend(reason_name):
        # Save to DB
        conn = sqlite3.connect("moods.db")
        conn.cursor().execute("INSERT INTO moods (emotion, reason) VALUES (?, ?)", (selected_emotion, reason_name))
        conn.commit()
        conn.close()

        # Get Song
        song_info = get_song(selected_emotion)

        # Update UI with the result
        # We remove old result boxes if they exist
        if len(page.controls) > 3:
            page.controls.pop()

        page.add(
            ft.Container(
                bgcolor="white", padding=20, border_radius=10, margin=ft.margin.only(top=20),
                content=ft.Column([
                    ft.Text(f"Saved: {selected_emotion} because of {reason_name}", color="black"),
                    ft.Text(f"🎵 Recommended: {song_info}", weight="bold", color="#ff4f87")
                ], horizontal_alignment="center")
            )
        )
        page.update()
    
    rows = []
    for emoji, reason_name in reasons:
        rows.append(ft.Column([
            ft.IconButton(content=ft.Text(emoji, size=40), on_click=lambda e, r=reason_name: save_and_recommend(r)),
            ft.Text(reason_name, size=12, color="#ff4f87")
        ], horizontal_alignment="center"))
    
    page.add(ft.Row(controls=rows, alignment="center"))
    page.update()

ft.app(target=main, assets_dir="assets")