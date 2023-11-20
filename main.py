import flet as ft
from utils import Neuro, g4f

generate_types = {
    "Текст" : Neuro.TEXT,
    "ID уровня" : Neuro.LEVEL,
    "ID/Ник игрока" : Neuro.USER
}

model_types = {
    "gpt3.5 long": g4f.models.gpt_35_long,
    "gpt3.5 turbo": g4f.models.gpt_35_turbo,
    "gpt4": g4f.models.gpt_4
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
        model = selectModel.value
        promt = textField.value

        page.client_storage.set('input', promt)
        page.client_storage.set('type', value)
        page.client_storage.set('model', model)

        neuroAnswer.value = 'Генерируем...'
        page.update()

        if value != None:
            neuro = Neuro(promt, generate_types[value], model_types[model])
        else:
            neuro = Neuro(promt, model=model_types[model])
        if neuro.answer != '您的免费额度不够使用这个模型啦，请点击右上角登录继续使用！':
            neuroAnswer.value = neuro.answer
        else:
            neuroAnswer.value = 'Ошибка, попробуйте заного.'
        neuroAnswer.tooltip = f"promt: {neuro.promt}\npromt_type: {neuro.promt_type}"

        mainRow.disabled = False
        page.update()

    textField = ft.TextField(hint_text="Запрос сюды", multiline=True, border_width=0, filled=True, expand=True, min_lines=4,
                             value=page.client_storage.get('input'))

    selectType = ft.Dropdown(options=[
        ft.dropdown.Option(i) for i in generate_types.keys()
    ], border_width=0, filled=True, border_radius=5, label='Тип', value=page.client_storage.get('type'), height=30, content_padding=0)
    selectModel = ft.Dropdown(options=[
       ft.dropdown.Option(text=i) for i in model_types.keys()
    ], border_width=0, filled=True, border_radius=5, label='Модель', value=page.client_storage.get('model'), height=30, content_padding=0)

    generateButton = ft.ElevatedButton('Сгенерировать', style=ft.ButtonStyle(
        shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=7),
               ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=2)}
    ), on_click=generate_click)
    neuroAnswer = ft.Markdown(selectable=True, auto_follow_links=True)

    page.add(title_bar,
             mainRow := ft.Row([
                 textField, 
                 ft.Column([
                            selectType,
                            selectModel,
                            generateButton
                            ])
                 ]),
            ft.Divider(),
            neuroAnswer
            )

ft.app(main)