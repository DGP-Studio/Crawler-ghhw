import time
# from urllib import request
import requests
import json
from bs4 import BeautifulSoup
from getMaterial import *


def GetResponse(url: str):
    """
    :param url: 武器页面的链接
    :return: 武器页面的源代码
    """
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        # "accept-encoding": "gzip, deflate, br",
        "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / "
                      "95.0.4638.54 Safari / 537.36 "
    }
    # req = request.Request(url=url, headers=headers)
    # response = request.urlopen(req)
    # contents = response.read().decode("utf-8")
    contents = requests.get(url)
    soup = BeautifulSoup(contents.text, "lxml")
    return soup


def GetWeaponInfo(url: str):
    """
    :param url: 武器页面的链接
    :return: 含有此武器所有信息的字典
    """
    soup = GetResponse(url)
    WeaponContent = soup.find("div", {"class": "wrappercont"})
    data = WeaponContent.find("div", {"class": "data_cont_wrapper", "style": "display: block"})
    # print(data)
    root = "https://genshin.honeyhunterworld.com"
    # 武器简介
    WeaponInfo = data.find("table", {"class": "item_main_table"})
    WeaponInfoDict = {}
    row = WeaponInfo.find_all("tr")
    for col in row:
        content = col.find_all("td")
        if len(content) == 3:  # type
            WeaponInfoDict["Type"] = content[2].text
            WeaponInfoDict["Source"] = content[0].find("img", {"class": "itempic lazy"})["data-src"]
        elif len(content) == 2:
            if content[0].text == "Rarity":
                WeaponInfoDict["Star"] = root + "/img/back/item/{}star.png".format(
                    len(content[1].find_all("div", {"class": "sea_char_stars_wrap"})))
            else:
                WeaponInfoDict[content[0].text] = content[1].text
    # print(WeaponInfoDict)
    # 武器基本数值 & 武器突破材料
    StatTable = data.find("span", {"class": "item_secondary_title"}, string=" Stat Progression ").find_next_sibling()
    WeaponStat = []
    row = StatTable.find_all("tr")
    table1, table2 = {}, {}
    for i in range(len(row)):
        content = row[i].find_all("td")
        # print(content)
        if i == 0:
            table1 = {
                "Name": "基础攻击力",
                "Value": {}
            }
            table2 = {
                "Name": content[2].text,
                "Value": {}
            }
            # print(temp1,temp2)
        elif i == len(row) - 3:  # 在Lv80+这一行获取武器突破材料
            table1["Value"][content[0].text] = content[1].text  # 等级
            if table2["Name"] == "元素精通":
                table2["Value"][content[0].text] = content[2].text  # 数值
            else:
                table2["Value"][content[0].text] = content[2].text + "%"  # 数值
            ContentMaterials = content[3]
            ContentMaterialsDiv = ContentMaterials.find_all("div", {"class": "itempic_cont lazy"})
            item_id_list = []
            for content in ContentMaterialsDiv[:-1]:
                # 获取材料的id,根据id找材料信息
                item_id = content.find("img", {"class": "itempic lazy"})["data-src"].split("/")[-1]
                item_id_list.append(item_id.split("_")[1])
            try:
                # 避免因为缺少突破材料导致报错
                Ascension = GetAscension(item_id_list[0])
                Elite = GetElite(item_id_list[1])
                Monster = GetMonster(item_id_list[2])
            except Exception:
                Ascension = {}
                Elite = {}
                Monster = {}
                print("本武器获取突破材料失败！")
            # print(Ascension)
            # print(Elite)
            # print(Monster)
        else:
            # print("正常写入")
            table1["Value"][content[0].text] = content[1].text  # 等级
            if table2["Name"] == "元素精通":
                table2["Value"][content[0].text] = content[2].text  # 数值
            else:
                table2["Value"][content[0].text] = content[2].text + "%"  # 数值
    WeaponStat.append(table1)
    WeaponStat.append(table2)
    # print(WeaponStat)
    # 武器副词条
    WeaponReline = {}
    RefineTable = StatTable.findNext("table", {"class": "add_stat_table"})
    row = RefineTable.find_all("tr")
    for i in range(1, len(row)):
        content = row[i].find_all("td")
        WeaponReline["Lv{}".format(i)] = content[1].text
    # print(WeaponReline)
    # 武器名字
    WeaponName = WeaponContent.find("div", {"class": "custom_title"}).text.replace("-", "").replace(" ", "")
    if WeaponName == "":
        try:
            # 实在获取不到只能在武器副词条处获取（再找不到就没办法了）
            # 此处的row = RefineTable.find_all("tr")
            WeaponName = row[0].find("span", {"class": "asc_amount"}).text.replace(" ", "")
        except Exception:
            WeaponName = ""
    # 武器背景故事
    try:
        Story = str(data.findNext("div", {"class": "story_container"}).getText)
        Story = Story.replace("<bound method Tag.get_text of <div class=\"story_container\"><br/>", "") \
            .replace("</div>>", "").replace("<br/>", "\n").rstrip("\n")
    except Exception:
        Story = ""
    # print(Story)
    # 武器英文名
    WeaponKey = GetWeaponKey(url)
    # print(WeaponKey)
    WeaponDict = {
        "Type": GetWeaponType(WeaponInfoDict["Type"]),
        "ATK": WeaponStat[0]["Value"]["90"],
        "SubStat": WeaponStat[1]["Name"],
        "SubStatValue": WeaponStat[1]["Value"]["90"],
        "Passive": WeaponInfoDict["Special (passive) Ability"],
        "PassiveDescription": WeaponReline,
        "Ascension": Ascension,
        "Elite": Elite,
        "Monster": Monster,
        "Name": WeaponName,
        "Star": WeaponInfoDict["Star"],
        "Key": WeaponKey,
        "Source": root + WeaponInfoDict["Source"],
        "Description": WeaponInfoDict["In-game Description"],
        "Story": Story,
        "WeaponStat": WeaponStat
    }
    return WeaponDict


def GetWeaponKey(url: str):
    soup = GetResponse(url.replace("CHS", "EN"))
    WeaponContent = soup.find("div", {"class": "wrappercont"})
    key = WeaponContent.find("div", {"class": "custom_title"}).text.replace("-", "").replace(" ", "").replace("'", "")
    if key == "":
        try:
            data = WeaponContent.find("div", {"class": "data_cont_wrapper", "style": "display: block"})
            title = data.find("span", {"class": "item_secondary_title"},
                              string=" Special Ability Progression (Refine) ")
            table = title.findNext("table", {"class": "add_stat_table"})
            key = table.find("tr").find("span", {"class": "asc_amount"}).text.replace("-", "").replace(" ", "").replace(
                "'", "")
        except Exception:
            key = ""
    return key


def GetWeaponType(type: str):
    dict = {
        "Sword": "https://genshin.honeyhunterworld.com/img/skills/s_33101.png",  # 单手剑
        "Claymore": "https://genshin.honeyhunterworld.com/img/skills/s_163101.png",  # 双手剑
        "Polearm": "https://genshin.honeyhunterworld.com/img/skills/s_233101.png",  # 长枪
        "Bow": "https://genshin.honeyhunterworld.com/img/skills/s_213101.png",  # 弓箭
        "Catalyst": "https://genshin.honeyhunterworld.com/img/skills/s_43101.png",  # 法器
    }
    return dict[type]


def GetWeaponUrl(WeaponType: str, Beta: bool = False):
    # 忽略的武器包括一星、二星武器，beta表格内无名武器，未上架到正服的武器
    IgnoreWeaponID = [
        "1001", "1101", "1406",
        "2001", "2101", "2204", "2406", "2407",
        "3001", "3101", "3204", "3404",
        "4001", "4101", "4201", "4403", "4405", "4406",
        "5001", "5101", "5201", "5404", "5404", "5405",
    ]
    root = "https://genshin.honeyhunterworld.com"
    soup = GetResponse(root + "/db/weapon/{}/?lang=CHS".format(WeaponType))
    data = soup.find("div", {"class": "wrappercont"})
    WeaponList = []
    if Beta is False:
        WeaponTable = data.find("span", {"class": "item_secondary_title"},
                                string="Released (Codex) Weapons").find_next_sibling()
    else:
        WeaponTable = data.find("span", {"class": "item_secondary_title"},
                                string="Unreleased, Incomplete or Upcoming Weapons").find_next_sibling()
    row = WeaponTable.find_all("tr")
    for i in range(1, len(row)):
        content = row[i].find_all("td")[2]
        # print(content)
        # WeaponSubStat = content[-1].text
        # WeaponName = content[0].find("a").text
        WeaponUrl = root + content.find("a")["href"]
        # WeaponStar = len(content[1].find_all("div", {"class": "stars_wrap"}))
        WeaponID = WeaponUrl.split("/")[-2].replace("w_", "")
        if WeaponID not in IgnoreWeaponID:
            WeaponList.append(WeaponUrl)
    return WeaponList


def GetAllWeaponUrl(Beta: bool = False):
    WeaponUrlList = []
    if Beta is False:
        Sword = GetWeaponUrl("Sword", False)
        Claymore = GetWeaponUrl("claymore", False)
        Polearm = GetWeaponUrl("polearm", False)
        Bow = GetWeaponUrl("bow", False)
        Catalyst = GetWeaponUrl("catalyst", False)
    else:
        Sword = GetWeaponUrl("Sword", True)
        Claymore = GetWeaponUrl("claymore", True)
        Polearm = GetWeaponUrl("polearm", True)
        Bow = GetWeaponUrl("bow", True)
        Catalyst = GetWeaponUrl("catalyst", True)
    WeaponUrlList.extend(Sword)
    WeaponUrlList.extend(Claymore)
    WeaponUrlList.extend(Polearm)
    WeaponUrlList.extend(Bow)
    WeaponUrlList.extend(Catalyst)
    # print("已获取到单手剑 {} 把".format(len(Sword)))
    # print("已获取到双手剑 {} 把".format(len(Claymore)))
    # print("已获取到长柄武器 {} 把".format(len(Polearm)))
    # print("已获取到弓 {} 把".format(len(Bow)))
    # print("已获取到法器 {} 把".format(len(Catalyst)))
    print("一共获取到 {} 把武器的链接".format(len(WeaponUrlList)))
    return WeaponUrlList


def GetAllWeapon(BetaWeapon: bool = False):
    if BetaWeapon:
        WeaponUrlList = GetAllWeaponUrl(Beta=True)
    else:
        WeaponUrlList = GetAllWeaponUrl()
    WeaponInfoList = []
    i = 0
    for url in WeaponUrlList:
        print("开始获取......")
        try:
            Weapon = GetWeaponInfo(url)
            WeaponInfoList.append(Weapon)
            i += 1
            print("{} {} 已获取！".format(i, Weapon["Name"]))
        except Exception as e:
            print("{} {} 获取失败！".format(i, url))
            print(e)
    print("已完成，一共获取到 {} 把武器的信息".format(len(WeaponInfoList)))
    return WeaponInfoList


if __name__ == "__main__":
    while True:
        print("=*=" * 15)
        print("1.获取全部武器信息")
        print("2.获取全部正服武器信息")
        print("3.获取全部beta武器信息")
        print("4.为weapons.json补充信息")
        print("退出请输入 # ")
        choice = str(input("请选择："))
        Weapon = None
        if choice is "#":
            exit()
        elif choice is "1":
            ReleaseWeapons = GetAllWeapon(BetaWeapon=False)
            BetaWeapons = GetAllWeapon(BetaWeapon=True)
            print("release:{}".format(len(ReleaseWeapons)))
            print("beta:{}".format(len(BetaWeapons)))
            ReleaseWeapons.extend(BetaWeapons)
            print("all:{}".format(len(ReleaseWeapons)))
            with open("./Weapons.json", "w", encoding="utf-8") as f:
                json.dump(ReleaseWeapons, f, ensure_ascii=False, indent=4)
            exit()
        elif choice is "2":
            ReleaseWeapons = GetAllWeapon(BetaWeapon=False)
            with open("./ReleaseWeapons.json", "w", encoding="utf-8") as f:
                json.dump(ReleaseWeapons, f, ensure_ascii=False, indent=4)
            exit()
        elif choice is "3":
            BetaWeapons = GetAllWeapon(BetaWeapon=True)
            with open("./BetaWeapons.json", "w", encoding="utf-8") as f:
                json.dump(BetaWeapons, f, ensure_ascii=False, indent=4)
            exit()
        elif choice is "4":
            url = str(input("请输入url:"))
            try:
                Weapon = GetWeaponInfo(url)
                print(" {} 已获取！".format(Weapon["Name"]))
                with open("./{}.json".format(Weapon["Key"]), "w", encoding="utf-8") as f:
                    json.dump(Weapon, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(" {} 获取失败！".format(url))
                print(e)
            exit()
        else:
            print("输入有误！请重新输入")
