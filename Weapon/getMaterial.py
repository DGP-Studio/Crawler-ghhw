def GetAscension(item_id):
    Ascension = {
        # 蒙德
        "504": {
            "City": "Mondstadt",
            "Name": "高塔孤王",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_Decarabian",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_504.png"
        },
        "524": {
            "City": "Mondstadt",
            "Name": "凛风奔狼",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_BorealWolf",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_524.png"
        },
        "544": {
            "City": "Mondstadt",
            "Name": "狮牙斗士",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_DandelionGladiator",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_544.png"
        },
        # 璃月
        "514": {
            "City": "Liyue",
            "Name": "孤云寒林",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_Guyun",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_514.png"
        },
        "534": {
            "City": "Liyue",
            "Name": "雾海云间",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_MistVeiled",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_534.png"
        },
        "554": {
            "City": "Liyue",
            "Name": "漆黑陨铁",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_Aerosiderite",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_554.png"
        },
        # 稻妻
        "564": {
            "City": "Inazuma",
            "Name": "远海夷地",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_DistantSea",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_564.png"
        },
        "574": {
            "City": "Inazuma",
            "Name": "鸣神御灵",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_Narukami",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_574.png"
        },
        "584": {
            "City": "Inazuma",
            "Name": "今昔剧画",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/5star.png",
            "Key": "Weapon_Mask",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/weapon/i_584.png"
        }
        # 须弥

    }

    if item_id not in Ascension.keys():
        return {}
    else:
        return Ascension[item_id]


def GetElite(item_id):
    Elite = {
        "63": {
            "Name": "号角",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_Horn",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_63.png"
        },
        "73": {
            "Name": "地脉",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_LeyLine",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_73.png"
        },
        "83": {
            "Name": "混沌",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_Chaos",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_83.png"
        },
        "93": {
            "Name": "雾虚",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_MistGrass",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_93.png"
        },
        "103": {
            "Name": "祭刀",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_SacrificialKnife",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_103.png"
        },
        "143": {
            "Name": "骨片",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_BoneShard",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_143.png"
        },
        "153": {
            "Name": "刻像",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_Statuette",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_153.png"
        },
        "173": {
            "Name": "混沌2",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_Chaos2",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_173.png"
        },
        "176": {
            "Name": "隐兽",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_Concealed",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_176.png"
        },
        "183": {
            "Name": "棱镜",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/4star.png",
            "Key": "Elite_Prism",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_183.png"
        },

    }

    if item_id not in Elite.keys():
        return {}
    else:
        return Elite[item_id]


def GetMonster(item_id):
    Monster = {
        "23": {
            "Name": "史莱姆",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Slime",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_23.png"
        },
        "33": {
            "Name": "面具",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Mask",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_33.png"
        },
        "43": {
            "Name": "绘卷",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Scroll",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_43.png"
        },
        "53": {
            "Name": "箭簇",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Scroll",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_43.png"
        },
        "113": {
            "Name": "徽记",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Insignia",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_113.png"
        },
        "123": {
            "Name": "鸦印",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_RavenInsignia",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_123.png"
        },
        "133": {
            "Name": "花蜜",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Nectar",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_133.png"
        },
        "163": {
            "Name": "刀镡",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Handguard",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_163.png"
        },
        "187": {
            "Name": "浮游",
            "Star": "https://genshin.honeyhunterworld.com/img/back/item/3star.png",
            "Key": "Monster_Spectral",
            "Source": "https://genshin.honeyhunterworld.com/img/upgrade/material/i_187.png"
        }
    }
    if item_id not in Monster.keys():
        return {}
    else:
        return Monster[item_id]
