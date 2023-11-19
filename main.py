import flet as ft
import flet_contrib
from utils import Neuro

generate_types = {
    "Текст" : Neuro.TEXT,
    "ID уровня" : Neuro.LEVEL,
    "ID игрока" : Neuro.USER
}

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window_title_bar_hidden = True
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.fonts = {
        'pusab' : "https://bestfonts.pro/fonts_files/6471afdbb5413d2287216815/files/Pusab.ttf",
        'rubik' : 'https://github.com/google/fonts/raw/main/ofl/rubik/Rubik%5Bwght%5D.ttf'
    }
    page.theme = ft.Theme(font_family='rubik')
    title_bar = ft.Row([
        ft.WindowDragArea(ft.Text("GDgpt beta", size = 30, font_family='pusab'), expand=True),
        ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda _: page.window_close())
    ])

    def generate_click(e):
        mainRow.disabled = True
        value = selectType.value
        promt = textField.value
        page.client_storage.set('input', promt)
        mainRow.update()

        if value != None:
            neuro = Neuro(promt, generate_types[value])
        else:
            neuro = Neuro(promt)
        neuroAnswer.value = neuro.answer
        neuroAnswer.tooltip = f"promt: {neuro.promt}\npromt_type: {neuro.promt_type}"

        mainRow.disabled = False
        page.update()

    textField = ft.TextField(hint_text="Запрос сюды", multiline=True, border_width=0, filled=True, expand=True, min_lines=3,
                             value=page.client_storage.get('input'))

    selectType = ft.Dropdown(options=[
        ft.dropdown.Option(text='Текст'),
        ft.dropdown.Option(text='ID уровня'),
        ft.dropdown.Option(text='ID игрока')
    ], border_width=0, filled=True, border_radius=5)

    generateButton = ft.ElevatedButton('Сгенерировать', style=ft.ButtonStyle(
        shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=7),
               ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=2)}
    ), on_click=generate_click)
    neuroAnswer = ft.Markdown(selectable=True)

    page.add(title_bar,
             mainRow := ft.Row([
                 textField, 
                 ft.Column([
                            selectType, 
                            generateButton
                            ])
                 ]),
            ft.Divider(),
            neuroAnswer
            )

ft.app(main)