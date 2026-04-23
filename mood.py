import flet as ft
import sqlite3
import requests

emotions_bad = [("😢", "Sad"), ("😠", "Angry"), ("😰", "Stressed"),  ("😞", "Overwhelmed"), ("🥱", "Tired") ]
emotions_Notgood = [("😴", "Unmotivated"), ("😔", "Insecure"), ("😒", "Annoyed"),  ("😅", "Disappointed"), ("🙃", "Bored") ]
emotions_neutral = [("🙂", "Okay"), ("😌", "Calm"), ("🤔", "Thoughtful"),  ("😀", "Fine"), ("😐", "Unbothered") ]
emotions_Good = [("😁", "Happy"), ("🫡", "Motivated"), ("☺️", "Proud"),  ("🫨", "Energized"), ("😇", "Peaceful") ]
emotions_Great = [("🤩", "Excited"), ("🥳", "Joyful"), ("🥰", "Loved"),  ("😜", "Passionate"), ("☺️", "Inspired") ]

reasons = [("💼", "Work"), ("👯", "Friends"), ("👨‍👩‍👧", "Family"), ("📚", "School"), ("💭", "Personal")]


def main(page: ft.Page):
    page.title = "Mood Tracker"
    page.window_width = 400
    page.window_height = 700

    page.bgcolor = "#ffd6e7"

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
            on_click = lambda e: survey(page, emotions_Notgood, "Not Good", show_moods)
        )
        
        neutral = ft.Container(content=ft.Image(
            src = "images/neutral.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_neutral, "Neutral", show_moods)
        )

        Good = ft.Container(content=ft.Image(
            src = "images/Good.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_Good, "Good", show_moods)
        )

        Great = ft.Container(content=ft.Image(
            src = "images/Great.PNG",
            width = 150,
            height = 150),
            on_click = lambda e: survey(page, emotions_Great, "Great", show_moods)
        )

        page.add(
            ft.Column(
                [ft.Text("Select your mood", size = 30, color="#ff4f87", weight = "bold"), 
                 ft.Row(controls=[Bad, Notgood, neutral, Good, Great])],
                horizontal_alignment="center"
            )
        )
        page.update()

    title = ft.Text(
            "Mood Tracker",
            size = 40,
            weight = "bold",
            color = "#ff4f87",
            text_align = "center",
        )
        
    subtitle = ft.Text(
            "How are you feeling today?",
            size = 18,
            color = "#444444",
            text_align = "center",
        )

    start_button = ft.ElevatedButton (
        text = "Start",
        bgcolor = "#ff8fb1",
        color = "white", 
        width = 150,
        height = 50,
        on_click = show_moods
    )

    page.add(
        ft.Container(
            content = ft.Column(
                [ title, subtitle, start_button],
                alignment = ft.MainAxisAlignment.CENTER, 
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 30
            ),
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

    rows = []
    for emoji, reason in reasons:
        rows.append(
            ft.Column([
                ft.IconButton(
                    content=ft.Text(emoji, size=40),
                    on_click= None
                ),
                ft.Text(reason,size=12, color="#ff4f87")
            ], horizontal_alignment="center")
        )
    page.add(ft.Row(controls=rows, alignment="center"))
    page.update()

#-------------------------------------------------------------------------------
#sql stuff

def database():
    conn = sqlite3.connect("moods.database")
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

def save_mood(emotion, reason):
    conn = sqlite3.connect("moods.database")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO moods (emotion, reason) VALUES (?, ?)", (emotion, reason))
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------
#API

def get_recommendation(emotion, reason):
    response = requests.get(
        "https://reccobeats.com/api/recommend", 
        params={"mood": emotion, "reason": reason})
  
    data = response.json() 
    
    return data.get("title"), data.get("artist")

ft.app(target = main, assets_dir="assets")