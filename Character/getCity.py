def getCharacterCity(characterKeyName):
    Mondstadt = [
        "albedo",
        "amber",
        "barbara",
        "bennett",
        "diluc",
        "diona",
        "eula",
        "fischl",
        "jean",
        "kaeya",
        "klee",
        "lisa",
        "mona",
        "noelle",
        "razor",
        "rosaria",
        "sucrose",
        "venti"
    ]
    Liyue = [
        "beidou",
        "chongyun",
        "ganyu",
        "hutao",
        "keqing",
        "ningguang",
        "qiqi",
        "shenhe",
        "tartaglia",
        "xiangling",
        "xiao",
        "xingqiu",
        "xinyan",
        "yanfei",
        "yunjin",
        "zhongli",
        "feiyan",
        "yelan"
    ]
    Inazuma = [
        "aloy",
        "itto",
        "gorou",
        "kazuha",
        "ayaka",
        "sara",
        "shougun",
        "kokomi",
        "sayu",
        "thoma",
        "yaemiko",
        "yoimiya",
        "ayato",
        "shinobu"
    ]
    characterKeyName = characterKeyName.lower()
    if characterKeyName in Mondstadt:
        return "https://upload-bbs.mihoyo.com/game_record/genshin/city_icon/UI_ChapterIcon_Mengde.png"
    elif characterKeyName in Liyue:
        return "https://upload-bbs.mihoyo.com/game_record/genshin/city_icon/UI_ChapterIcon_Liyue.png"
    elif characterKeyName in Inazuma:
        return "https://upload-bbs.mihoyo.com/game_record/genshin/city_icon/UI_ChapterIcon_Daoqi.png"
    else:
        return "ERROR: CANNOT FIND CHARACTER CITY"


def getTalentCity(TalentName):
    Mondstadt = [
        "诗文",
        "自由",
        "抗争"
    ]
    Liyue = [
        "勤劳",
        "黄金",
        "繁荣"
    ]
    Inazuma = [
        "浮世",
        "风雅",
        "天光"
    ]
    if TalentName in Mondstadt:
        return "Mondstadt"
    elif TalentName in Liyue:
        return "Liyue"
    elif TalentName in Inazuma:
        return "Inazuma"
    else:
        return "ERROR: CANNOT FIND TALENT CITY"


def getWeeklyItemName(WeeklyItemName):
    Mondstadt = [
        "东风之翎",
        "东风之爪",
        "东风的吐息",
        "北风之尾",
        "北风之环",
        "北风的魂匣"
    ]
    Liyue = [
        "吞天之鲸·只角",
        "魔王之刃·残片",
        "武炼之魂·孤影",
        "龙王之冕",
        "血玉之枝",
        "鎏金之鳞"
    ]
    Inazuma = [
        "熔毁之刻",
        "狱火之蝶",
        "灰烬之心",
        "凶将之手眼",
        "祸神之禊泪",
        "万劫之真意"
    ]
    if WeeklyItemName in Mondstadt:
        return "Mondstadt"
    elif WeeklyItemName in Liyue:
        return "Liyue"
    elif WeeklyItemName in Inazuma:
        return "Inazuma"
    else:
        return "ERROR: CANNOT FIND WEEKLY ITEM CITY"
