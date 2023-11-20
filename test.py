import gdshechka

find = gdshechka.FindLevelByName("white space").find_first
print(gdshechka.Level(find["id"]).api)