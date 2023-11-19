import g4f, gd, asyncio

async def get_level_info(ide: int):
    cilent = gd.Client()

    level = await cilent.get_level(ide)
    return f"""name: {level.name},
        creator: {level.creator},
        description: {level.description},
        difficulty: {level.difficulty},
        downloads: {level.downloads},
        rating: {level.rating},
        song: {level.song},
        coins: {level.coins},
        password: {level.password_data}"""

async def get_user_info(id: int):
    cilent = gd.Client()
    user = await cilent.get_user(id)

    return f"""username: {user.name},
    socials: {user.socials},
    states: {user.states},
    comments: {user.get_comments(1).all}
    """

class Neuro:
    TEXT = 'text'
    LEVEL = 'level'
    USER = 'user'
    
    def call(promt: str):
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_long,
            messages=[{"role": "user", "content": promt}],
        )
        return response
    
    def __init__(self, promt: str, promt_type: str = 'text') -> str:
        self.promt = promt
        self.promt_type = promt_type

        if promt_type == Neuro.LEVEL:
            result = []
            for i in self.promt.split(' '):
                try:
                    i = int(i)
                    level = asyncio.run(get_level_info(i))
                    result.append(level.strip())
                except:
                    result.append(i)
            self.answer = Neuro.call(" ".join(result)) 
        elif promt_type == Neuro.USER:
            result = []
            for i in self.promt.split(' '):
                try:
                    i = int(i)
                    level = asyncio.run(get_user_info(i))
                    result.append(level.strip())
                except:
                    result.append(i)
            print(result)
            self.answer = Neuro.call(" ".join(result))
        else:
            self.answer = Neuro.call(self.promt)