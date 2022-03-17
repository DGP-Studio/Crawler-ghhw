import time
from urllib import request
from bs4 import BeautifulSoup
import json


def GetResponse(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        # "accept-encoding": "gzip, deflate, br",
        "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / "
                      "95.0.4638.54 Safari / 537.36 "
    }
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    contents = response.read().decode("utf-8")
    soup = BeautifulSoup(contents, "lxml")
    return soup


def GetWeaponInfo(url):
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
    # 武器基本数值
    StatTable = data.find("span", {"class": "item_secondary_title"}, string=" Stat Progression ").find_next_sibling()
    WeaponStat = []
    row = StatTable.find_all("tr")
    for i in range(len(row)):
        content = row[i].find_all("td")
        # print(content)
        if i == 0:
            temp1 = {
                "Name": "攻击力",
                "Value": {}
            }
            temp2 = {
                "Name": content[2].text,
                "Value": {}
            }
            # print(temp1,temp2)
        elif i == len(row) - 3:  # 在lv80这一行获取武器突破材料
            temp1["Value"][content[0].text] = content[1].text
            temp2["Value"][content[0].text] = content[2].text
            ContentMaterials = content[3]
            ContentMaterialsDiv = ContentMaterials.find_all("div", {"class": "itempic_cont lazy"})
            temp3 = [{}, {}, {}]
            for content, item in zip(ContentMaterialsDiv[:-1], temp3):
                # print(content)
                item["Star"] = root + content["data-bg"].replace("url('", "").replace("')", "")
                item["Source"] = root + content.find("img", {"class": "itempic lazy"})["data-src"].replace("_35.png",
                                                                                                           ".png")
                # 获取材料名称需要再次发送请求
                SourceID = item["Source"].split("/")[-1].replace(".png", "")
                item["Name"] = GetWeaponSourceName(root + "/db/item/{}/?lang=CHS".format(SourceID))[0:4]
                item["Key"] = GetWeaponSourceName(root + "/db/item/{}/?lang=EN".format(SourceID)).replace(" ", "")
            Ascension, Elite, Monster = temp3
            Ascension["City"] = GetWeaponSourceCity(Ascension["Name"])
            # print(Ascension)
            # print(Elite)
            # print(Monster)
        else:
            # print("正常写入")
            temp1["Value"][content[0].text] = content[1].text
            temp2["Value"][content[0].text] = content[2].text
    WeaponStat.append(temp1)
    WeaponStat.append(temp2)
    # print(WeaponStat)
    # 武器副词条
    WeaponReline = {}
    RefineTable = StatTable.findNext("table", {"class": "add_stat_table"})
    row = RefineTable.find_all("tr")
    # 武器名字
    WeaponName = WeaponContent.find("div", {"class": "custom_title"}).text.replace("-", "").replace(" ", "")
    if WeaponName == "":
        try:
            WeaponName = row[0].find("span", {"class": "asc_amount"}).text.replace(" ", "")
        except Exception:
            WeaponName = ""
    for i in range(1, len(row)):
        content = row[i].find_all("td")
        WeaponReline["Lv{}".format(i)] = content[1].text
    # print(WeaponReline)
    # 武器背景故事
    try:
        Story = str(data.findNext("div", {"class": "story_container"}).getText)
        Story = Story.replace("<bound method Tag.get_text of <div class=\"story_container\"><br/>", "") \
            .replace("</div>>", "").replace("<br/>", "\n")
    except Exception:
        Story = ""
    # print(Story)
    # 武器英文名
    WeaponKey = GetWeaponKey(url)
    # print(WeaponKey)
    Weapon = {
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

    return Weapon


def GetWeaponKey(url):
    soup = GetResponse(url.replace("CHS", "EN"))
    WeaponContent = soup.find("div", {"class": "wrappercont"})
    key = WeaponContent.find("div", {"class": "custom_title"}).text.replace("-", "").replace(" ", "")
    if key == "":
        try:
            data = WeaponContent.find("div", {"class": "data_cont_wrapper", "style": "display: block"})
            title = data.find("span", {"class": "item_secondary_title"}, string=" Special Ability Progression (Refine) ")
            table = title.findNext("table", {"class": "add_stat_table"})
            key = table.find("tr").find("span", {"class": "asc_amount"}).text.replace("-", "").replace(" ", "")
        except Exception:
            key = ""
    return key


def GetWeaponSourceName(url):
    soup = GetResponse(url)
    name = soup.find("div", {"class": "custom_title"}).text
    return name


def GetWeaponSourceCity(WeaponItemName):
    # 蒙德
    Mondstadt = ["高塔孤王", "凛风奔狼", "狮牙斗士"]
    # 璃月
    Liyue = ["孤云寒林", "雾海云间", "漆黑陨铁"]
    # 稻妻
    Inazuma = ["远海夷地", "鸣神御灵", "今昔剧画"]
    if WeaponItemName in Mondstadt:
        return "Mondstadt"
    elif WeaponItemName in Liyue:
        return "Liyue"
    elif WeaponItemName in Inazuma:
        return "Inazuma"
    else:
        return "Error"


def GetWeaponType(type):
    dict = {
        "Sword": "https://genshin.honeyhunterworld.com/img/skills/s_33101.png",  # 单手剑
        "Claymore": "https://genshin.honeyhunterworld.com/img/skills/s_163101.png",  # 双手剑
        "Polearm": "https://genshin.honeyhunterworld.com/img/skills/s_233101.png",  # 长枪
        "Bow": "https://genshin.honeyhunterworld.com/img/skills/s_213101.png",  # 弓箭
        "Catalyst": "https://genshin.honeyhunterworld.com/img/skills/s_43101.png",  # 法器
    }
    return dict[type]


def GetWeaponUrl(WeaponType, Beta=False):
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
    WeaponTable = data.find("span", {"class": "item_secondary_title"},
                            string="Released (Codex) Weapons").find_next_sibling()
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
    if Beta is True:
        BetaWeaponTable = data.find("span", {"class": "item_secondary_title"},
                                    string="Unreleased, Incomplete or Upcoming Weapons").find_next_sibling()
        row = BetaWeaponTable.find_all("tr")
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
        # print(WeaponList,len(WeaponList))
        return WeaponList
    else:
        return WeaponList


def GetAllWeaponUrl():
    AllWeaponList = []
    Sword = GetWeaponUrl("Sword", True)
    Claymore = GetWeaponUrl("claymore", True)
    Polearm = GetWeaponUrl("polearm", True)
    Bow = GetWeaponUrl("bow", True)
    Catalyst = GetWeaponUrl("catalyst", True)
    AllWeaponList.extend(Sword)
    AllWeaponList.extend(Claymore)
    AllWeaponList.extend(Polearm)
    AllWeaponList.extend(Bow)
    AllWeaponList.extend(Catalyst)
    print("已获取到单手剑 {} 把".format(len(Sword)))
    print("已获取到双手剑 {} 把".format(len(Claymore)))
    print("已获取到长柄武器 {} 把".format(len(Polearm)))
    print("已获取到弓 {} 把".format(len(Bow)))
    print("已获取到法器 {} 把".format(len(Catalyst)))
    print("一共获取到 {} 把武器的链接".format(len(AllWeaponList)))
    return AllWeaponList


if __name__ == "__main__":
    while True:
        print("=*=" * 15)
        print("1.获取指定武器信息")
        print("2.获取全部武器信息")
        print("3.为weapons.json补充信息")
        print("退出请输入 # ")
        choice = str(input("请选择："))
        if choice is "#":
            exit()
        elif choice is "1":
            url = str(input("请输入武器的url："))
            print("开始获取......")
            try:
                Weapon = GetWeaponInfo(url)
                with open("{}.json".format(Weapon["Key"]), "w", encoding="utf-8") as f:
                    json.dump(Weapon, f, ensure_ascii=False, indent=4)
                print("{0} 获取完成！输出文件名为 {1}.json".format(Weapon["Name"], Weapon["Key"]))
            except Exception as e:
                print("获取失败！")
                print(e)
                # exit()
        elif choice is "2":
            AllWeaponList = GetAllWeaponUrl()
            i = 0
            WeaponInfoList = []
            for url in AllWeaponList:
                print("开始获取......")
                i += 1
                try:
                    Weapon = GetWeaponInfo(url)
                    WeaponInfoList.append(Weapon)
                    with open("example.json", "w", encoding="utf-8") as f:
                        json.dump(WeaponInfoList, f, ensure_ascii=False, indent=4)
                    print("{0} {1} 已经获取成功！".format(i, Weapon["Name"]))
                except Exception as e:
                    i -= 1
                    print("{0} {1} 获取失败！".format(i, url))
                    print(e)
                time.sleep(1)
            print("获取完毕！一共获取到 {0} 把武器，成功获取 {1} 把武器的信息".format(len(AllWeaponList), i))
            exit()
        elif choice is "3":
            try:
                with open("weapons.json", "r", encoding="utf-8") as f:
                    WeaponList = json.load(f)
                print("已获取到 {} 把武器的信息".format(len(WeaponList)))
            except Exception as e:
                print("e")
                exit()
            WeaponDict = {}
            for i in range(len(WeaponList)):
                WeaponDict[WeaponList[i]["Name"]] = i
            # print(WeaponDict)
            AllWeaponList = GetAllWeaponUrl()
            i = 0
            for url in AllWeaponList:
                # print("开始获取......")
                i += 1
                try:
                    Weapon = GetWeaponInfo(url)
                    weapon_id = WeaponDict[Weapon["Name"]]
                    WeaponList[weapon_id]["PassiveDescription"] = Weapon["PassiveDescription"]
                    WeaponList[weapon_id]["Description"] = Weapon["Description"]
                    WeaponList[weapon_id]["Story"] = Weapon["Story"]
                    WeaponList[weapon_id]["WeaponStat"] = Weapon["WeaponStat"]
                    with open("weapons_new.json", "w", encoding="utf-8") as f:
                        json.dump(WeaponList, f, ensure_ascii=False, indent=4)
                    print("{0} {1} {2} 已经补充成功！".format(i, weapon_id, Weapon["Name"]))
                except Exception as e:
                    i -= 1
                    print("{0} {1} 补充失败！".format(i, url))
                    print(e)
                time.sleep(1)
            print("修改完毕！一共获取到 {0} 把武器的信息，成功补充 {1} 把武器的信息".format(len(WeaponList), i))
            exit()
        else:
            print("输入有误！请重新输入")