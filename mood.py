import flet as ft
import sqlite3
import requests
import random

emotions_bad = [("😢", "Sad"), ("😠", "Angry"), ("😰", "Stressed"),  ("😞", "Overwhelmed"), ("🥱", "Tired") ]
emotions_Notgood = [("😴", "Unmotivated"), ("😔", "Insecure"), ("😒", "Annoyed"),  ("😅", "Disappointed"), ("🙃", "Bored") ]
emotions_neutral = [("🙂", "Okay"), ("😌", "Calm"), ("🤔", "Thoughtful"),  ("😀", "Fine"), ("😐", "Unbothered") ]
emotions_Good = [("😁", "Happy"), ("🫡", "Motivated"), ("☺️", "Proud"),  ("🫨", "Energized"), ("😇", "Peaceful") ]
emotions_Great = [("🤩", "Excited"), ("🥳", "Joyful"), ("🥰", "Loved"),  ("😜", "Passionate"), ("☺️", "Inspired") ]

reasons = [("💼", "Work"), ("👯", "Friends"), ("👨‍👩‍👧", "Family"), ("📚", "School"), ("💭", "Personal")]

def database():
    conn = sqlite3.connect("moods.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT,
            reason TEXT,
            note TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP)
            """)
    try:
        cursor.execute("ALTER TABLE moods ADD COLUMN note TEXT")
    except:
        pass
    conn.commit()
    conn.close()

def get_song(mood):
    try:
        url = f"https://itunes.apple.com/search?term={mood}+music&limit=50&entity=song"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data["resultCount"] > 0:
            random_song = random.choice(data["results"])
            song_name = random_song["trackName"]
            artist = random_song["artistName"]
            return f"{song_name} by {artist}"
    except:
        pass
    return "No song found..."

def get_history_controls():
    conn = sqlite3.connect("moods.db")
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, reason, note, date FROM moods ORDER BY date DESC")
    history = cursor.fetchall()
    conn.close()

    history_controls = []

    if len(history) == 0: 
        history_controls.append(
            ft.Text("No moods saved yet.", size=16, color="#444444"))
    else:
        for emotion, reason, note, date in history:
            history_controls.append(
                ft.Container( 
                    bgcolor= "white",
                    padding=15,
                    border_radius=10,
                    margin=ft.margin.only(bottom=10),
                    content=ft.Column(
                        [ft.Text(f"Feeling: {emotion}", color="black", weight="bold"),
                            ft.Text(f"Reason: {reason}", color="black"),
                            ft.Text(f"Note: {note}", color="black"),
                            ft.Text(f"Date: {date}", color="#777777", size=12)])))

    return history_controls

def main(page: ft.Page):
    page.title = "Mood Tracker"
    page.window_width = 400
    page.window_height = 700

    page.bgcolor = "#ffd6e7"
    database()


    def show_moods(e):
        page.controls.clear()

        Bad = ft.Container(content=ft.Image(
            src = "images/Bad.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_bad, "Bad", show_moods))

        Notgood = ft.Container(content=ft.Image(
            src = "images/Notgood.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_Notgood, "Not Good", show_moods))
        
        neutral = ft.Container(content=ft.Image(
            src = "images/neutral.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_neutral, "Neutral", show_moods))

        Good = ft.Container(content=ft.Image(
            src = "images/Good.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_Good, "Good", show_moods))

        Great = ft.Container(content=ft.Image(
            src = "images/Great.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_Great, "Great", show_moods))

        tabs = ft.Tabs(
            selected_index=0,
            expand=True,
            tabs=[
                ft.Tab(
                    text="Mood",
                    content=ft.Column(
                        [ft.Text("Select your mood", size=30, color="#ff4f87", weight="bold"),
                            ft.Row(controls=[Bad, Notgood, neutral, Good, Great], scroll="auto")],
                        horizontal_alignment="center")),
                ft.Tab(
                    text="History",
                    content=ft.Column(
                    controls=get_history_controls(),
                    scroll="auto", expand=True))])

        page.add(tabs)
        page.update()

    title = ft.Text(
            "Mood Tracker",
            size = 40,
            weight = "bold",
            color = "#ff4f87",
            text_align = "center")
        
    subtitle = ft.Text(
            "How are you feeling today?",
            size = 18,
            color = "#444444",
            text_align = "center")

    start_button = ft.ElevatedButton (
        text = "Start",
        bgcolor = "#ff8fb1",
        color = "white", 
        width = 150,
        height = 50,
        on_click = show_moods)

    page.add(
        ft.Container(
            content = ft.Column(
                [title, subtitle, start_button],
                alignment = ft.MainAxisAlignment.CENTER, 
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 30),
            alignment = ft.alignment.center,
            expand =  True
        )
    )
#-------------------------------------------------------------------------------

def survey(page, emotion_list, label, go_back):
    page.controls.clear()

    back_button = ft.TextButton("Back", style=ft.ButtonStyle(color="#ff4f87"), 
                                on_click=lambda e: go_back(e))
    page.add(back_button)

    def log(mood):
        page.snack_bar = ft.SnackBar(ft.Text(f"Saved {mood}!"))
        page.snack_bar.open = True
        page.update()

    page.add(ft.Text("What is your specific feeling?", size=20, color="#ff4f87", weight="bold", ))

    rows = []
    for emoji, name in emotion_list:
        rows.append(ft.Column([ft.IconButton(content=ft.Text(emoji, size=40),
                                on_click=lambda e, name=name: show_reasons(page, name, 
                                lambda e: survey(page, emotion_list, label, go_back))),
                                ft.Text(name, size=12, color="#ff4f87")], 
                                horizontal_alignment="center"))
        
    page.add(ft.Row(controls=rows, alignment="center"))
    page.update()

def show_reasons(page, selected_emotion, go_back):
    page.controls.clear()

    back_button= ft.TextButton("Back", style=ft.ButtonStyle(color="#ff4f87"), 
                                on_click=lambda e: go_back(e))
    page.add(back_button)

    page.add(ft.Text("Why do you feel this way?", size=20, color= "#ff4f87", weight="bold" ))

    note_box = ft.TextField(
        label="Note about your day", color="#808080", border_color="#A9A9A9", cursor_color= "#808080", 
        label_style=ft.TextStyle(color="#808080"))
    page.add(note_box)

    def save_and_recommend(reason_name):
        conn = sqlite3.connect("moods.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO moods (emotion, reason, note) VALUES (?, ?, ?)", (selected_emotion, reason_name, note_box.value))
        conn.commit()
        conn.close()

        song_info = get_song(selected_emotion)

        if len(page.controls) > 4:
            page.controls.pop()

        page.add(
            ft.Row(
            controls=[ft.Container(
                bgcolor="white", 
                padding=20, 
                border_radius=10, 
                margin=ft.margin.only(top=20),
                content=ft.Column([
                    ft.Text(f"Saved: {selected_emotion} because of {reason_name}", color="black"),
                    ft.Text(f"🎵 Recommended: {song_info}", weight="bold", color="#ff4f87")],
                    horizontal_alignment="center", tight=True))],
                    alignment=ft.MainAxisAlignment.CENTER))
        
        page.update()
    
    rows = []
    for emoji, reason_name in reasons:
        rows.append(ft.Column([ft.IconButton(content=ft.Text(emoji, size=40), 
        on_click=lambda e, r=reason_name: save_and_recommend(r)),
        ft.Text(reason_name, size=12, color="#ff4f87")], horizontal_alignment="center"))
    
    page.add(ft.Row(controls=rows, alignment="center"))
    page.update()

ft.app(target = main, assets_dir="assets")