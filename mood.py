import flet as ft

def main(page: ft.Page):
    page.title = "Mood Tracker"
    page.window_width = 400
    page.window_height = 700

    page.bgcolor = "#ffd6e7"

    def show_moods(e):
        page.controls.clear()

        Bad = ft.Image(
            src = "images/Bad.PNG",
            width = 150,
            height = 150,
            #on_click = lambda e: survey(e, "Bad")
        )

        Notgood = ft.Image(
            src = "images/Notgood.PNG",
            width = 150,
            height = 150,
            #on_click = lambda e: survey(e, "Not Good")
        )
        
        neutral = ft.Image(
            src = "images/neutral.PNG",
            width = 150,
            height = 150,
            #on_click = lambda e: survey(e, "Neutral")
        )

        Good = ft.Image(
            src = "images/Good.PNG",
            width = 150,
            height = 150,
            #on_click = lambda e: survey(e, "Good")
        )

        Great = ft.Image(
            src = "images/Great.PNG",
            width = 150,
            height = 150,
            #on_click = lambda e: survey(e, "Great")
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
#-------------------------------------------------------

def create_emoji(emoji, label):
    return ft.Column(controls=[ft.IconButton(content=ft.Text(emoji, size=40), 
    on_click=lambda _: log(label)), ft.Text(label, size = 12, color = "#ff4f87")],
    horizontal_alignment = ft.CrossAxisAlignment.CENTER)

def survey(page):
    page.controls.clear()

    def log(mood):
        page.add(ft.SnackBar(ft.Text(f"Saved {mood}!")))
        page.update()

    emotions = [("😊", "Happy"), ("😐", "Okay"), ("🧘", "Calm"), ("🙏", "Grateful"),
        ("😌", "Content"), ("😢", "Sad"), ("😌", "Relaxed"), ("😟", "Worried"),
        ("😠", "Angry"), ("😰", "Stressed"), ("😴", "Tired")]

    page.update()

ft.app(target = main, assets_dir="assets")