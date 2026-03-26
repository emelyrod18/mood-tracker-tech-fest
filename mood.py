import flet as ft

def main(page: ft.Page):
    page.title = "Mood Tracker"
    page.window_width = 400
    page.window_height = 700

    page.bgcolor = "#ffd6e7"

    def show_moods(e):
        page.clean()

        Bad = ft.Image(
            src = "Bad.PNG",
            width = 120,
            height = 120,
            on_click = lambda e: print("bad selected")
        )

        Notgood = ft.Image(
            src = "Notgood.PNG",
            width = 120,
            height = 120,
            on_click = lambda e: print("Not good selected")
        )

        page.add(
            ft.Column(
                [ft.Text("Select your mood", size = 30), ft.Row([Bad, Notgood])],
                horizontal_alignment="center"
            )
        )
    
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

ft.app(target = main)
