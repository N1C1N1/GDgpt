import g4f, gdshechka, json

class Neuro:
    TEXT = 'text'
    LEVEL = 'level'
    USER = 'user'
    
    def call(promt: str, model: g4f.models = g4f.models.gpt_35_long):
        print(promt)
        try:
            response = g4f.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "user", "content": "следующий вопрос будет по игре Geometry dash, отвечай на русском"},
                    {"role": "user", "content": promt}
                    ]
            )
        except:
            return "Ошибка генерации, попробуйте выбрать другую модель."
        return response
    
    def __init__(self, promt: str, promt_type: str = 'text', model: g4f.models = g4f.models.gpt_35_long) -> str:
        self.promt = promt
        self.promt_type = promt_type
        self.model = model

        # Строка что бы была, всё равно исходники никто чекать не будет. С.И.С.И
        if promt_type == Neuro.LEVEL:
            result = []
            for i in self.promt.split('"'):
                try:
                    i = int(i)
                    level = gdshechka.Level(i).api
                    result.append(json.dumps(level))
                except:
                    try:
                        level = gdshechka.Level(gdshechka.FindLevelByName(str(i)).find_first["id"]).api
                        if level["name"] != 'ReTraY':
                            result.append(json.dumps(level))
                        else:
                            result.append(i)
                    except:
                        result.append(i)
            self.answer = Neuro.call(" ".join(result), model) 

        elif promt_type == Neuro.USER:
            result = []
            for i in self.promt.split('"'):
                user = gdshechka.Account(i).api
                if user["name"] != ' ':
                    result.append(json.dumps(user))
                else:
                    result.append(i)
            self.answer = Neuro.call(" ".join(result), model)
        else:
            self.answer = Neuro.call(self.promt, model)