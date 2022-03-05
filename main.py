import time
import requests
import re
from bs4 import BeautifulSoup
import json


def getCharInfo(url):
    global CharTitle, charAstrolabeName, charDescription
    URL_Prefix = "https://genshin.honeyhunterworld.com/"
    #print("=" * 20)
    keyword_pattern = "(\/char\/)(\w)+(\/)"
    re_result = re.search(keyword_pattern, url).group()
    re_result = re_result.replace("/char/", "")
    charKeyword = re_result.replace("/", "").capitalize()
    #print("charKeyword: " + charKeyword)
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "referer": "https://genshin.honeyhunterworld.com/db/char/amber/?lang=EN",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    # 获取主要信息页面
    main_content = soup.find("div", {'class': 'wrappercont'})
    #print(main_content)
    # 获取角色名称
    charName = main_content.find('div', {'class': 'custom_title'}).text
    #print("charName: " + charName)

    # 角色信息表格
    charInfoTable = main_content.find('table', {'class': 'item_main_table'}).find_all('tr')
    # 角色信息表格
    for item in charInfoTable:
        this_line = item.find_all('td')
        # 角色 Title
        if this_line[0].text == "Title":
            CharTitle = this_line[1].text
            #print("CharTitle: " + CharTitle)
        if this_line[0].text == "Allegiance":
            CharAllegiance = this_line[1].text
            #print("CharAllegiance: " + CharAllegiance)
        if this_line[0].text == "Rarity":
            charRarity = len(this_line[1].find_all('div', {'class': 'sea_char_stars_wrap'}))
            #print("charRarity: " + str(charRarity))
        if this_line[0].text == "Element":
            charElementPicURL = URL_Prefix + this_line[1].find('img')['data-src'].replace("_35", "")
            charElementPicURL = charElementPicURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
            #print("charElement: " + str(charElementPicURL))
        if this_line[0].text == "Astrolabe Name":
            charAstrolabeName = this_line[1].text
            #print("charAstrolabeName: " + charAstrolabeName)
        if this_line[0].text == "In-game Description":
            charDescription = this_line[1].text
            #print("charDescription: " + charDescription)

    # 角色属性表格
    #print("=" * 20 + "\n角色属性")
    skilldmgwrapper = main_content.find('div', {'class': 'skilldmgwrapper'}).find_all('tr')
    charTableList = []
    skilldmgwrapp_table1 = []
    skilldmgwrapp_table2 = []
    skilldmgwrapp_table3 = []
    skilldmgwrapp_table4 = []
    skilldmgwrapp_table5 = []
    skilldmgwrapp_table6 = []
    skilldmgwrapp_table7 = []
    for eachLine in skilldmgwrapper:
        all_prop = eachLine.find_all('td')
        skilldmgwrapp_table1.append(all_prop[0].text)
        skilldmgwrapp_table2.append(all_prop[1].text)
        skilldmgwrapp_table3.append(all_prop[2].text)
        skilldmgwrapp_table4.append(all_prop[3].text)
        skilldmgwrapp_table5.append(all_prop[4].text)
        skilldmgwrapp_table6.append(all_prop[5].text)
        try:
            skilldmgwrapp_table7.append(all_prop[6].text)
        except:
            pass
            #print("This character only has 6 stat")
    charTableList.append(skilldmgwrapp_table1)
    charTableList.append(skilldmgwrapp_table2)
    charTableList.append(skilldmgwrapp_table3)
    charTableList.append(skilldmgwrapp_table4)
    charTableList.append(skilldmgwrapp_table5)
    charTableList.append(skilldmgwrapp_table6)
    if skilldmgwrapp_table7 == []:
        charTableList.append(skilldmgwrapp_table7)

    charStatList = []
    for list in charTableList:
        if list[0] != "Lv":
            i = 1
            this_stat_dict = {}
            this_stat_dict['Name'] = list[0]
            this_stat_set = {}
            while i < len(list):
                this_stat_set[charTableList[0][i]] = list[i]
                # this_dict[charTableList[0][i]] = list[i] # 旧方案
                i += 1
            this_stat_dict["Values"] = this_stat_set
            charStatList.append(this_stat_dict)
    charTableJson = json.dumps(charStatList, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    charTableJson = charStatList
    #print(charTableJson)

    # 命之座 Constellations
    #print("=" * 20)
    #print("命之座")
    ConstellationsDict = {}
    Constellations_list = []
    Constellations_title = main_content.find('span', {'class': 'item_secondary_title'}, string="Constellations")
    Constellations_table = Constellations_title.findNext('table', {'class': 'item_main_table'}).find_all('tr')
    # 每两行一个命之座
    Constellations_list_count = 0
    while Constellations_list_count < len(Constellations_table):
        this_Constellations = {
            "Source": "",
            "Name": "",
            "Description": ""
        }
        if (Constellations_list_count + 1) % 2 != 0:
            # print("This is a start of a constellation")
            this_line = Constellations_table[Constellations_list_count]
            imageURL = URL_Prefix + this_line.find_all('img', {'class': 'itempic'})[-1]['data-src']
            imageURL = imageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
            # print("imgURL: " + str(imageURL))
            ConstellationsName = this_line.find_all('a', href=re.compile("/db/skill"))[-1].text
            # print("ConstellationsName: " + ConstellationsName)
            this_line = Constellations_table[Constellations_list_count + 1]
            ConstellationsDesc = this_line.find('div', {'class': 'skill_desc_layout'}).text
            # print("ConstellationsDesc: " + ConstellationsDesc)

            # Add to list
            this_Constellations['Source'] = imageURL
            this_Constellations['Name'] = ConstellationsName
            this_Constellations['Description'] = ConstellationsDesc
            Constellations_list.append(this_Constellations)
        Constellations_list_count += 2
    #print(Constellations_list)
    ## 生成Json
    Constellation = 0
    while Constellation < len(Constellations_list):
        keyName = "Constellations" + str(Constellation + 1)
        ConstellationsDict[keyName] = Constellations_list[Constellation]
        Constellation += 1
    Constellations_Json = json.dumps(ConstellationsDict, ensure_ascii=False, sort_keys=True, indent=4,
                                     separators=(',', ':'))
    Constellations_Json = ConstellationsDict
    # print(Constellations_Json)

    # 技能
    skillsTitle = main_content.find('span', string='Attack Talents')

    ## 普攻
    #print("=" * 20 + "\n普攻")
    normalAttack = {}
    normal_attack_area = skillsTitle.find_next_sibling()
    normal_attack_info = normal_attack_area.find_all('tr')
    normalAttack_imageURL = URL_Prefix + normal_attack_info[0].find('img', {'class': 'itempic'})['data-src']
    normalAttack_imageURL = normalAttack_imageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
    # print("imageURL: " + normalAttack_imageURL)
    normalAttack_name = normal_attack_info[0].find('a', href=re.compile('/db/skill/')).text
    # print("attack_name: " + str(normalAttack_name))
    normalAttack_desc = normal_attack_info[1].find('div', {'class': 'skill_desc_layout'}).text.replace(" ", "\n")
    # print("normalAttack_desc: " + str(normalAttack_desc))
    ### 表格
    normalAttack_table_list = []
    normalAttack_table_area = normal_attack_area.find_next_sibling()
    normalAttack_table = normalAttack_table_area.find_all('tr')
    for eachLine in normalAttack_table:
        this_line_list = []
        all_columns = eachLine.find_all('td')
        for each_column in all_columns:
            this_item = each_column.text
            this_line_list.append(this_item)
        normalAttack_table_list.append(this_line_list)
    '''
    for item in normalAttack_table_list:
        print(item)
    '''
    ## 生成字典
    # print(normalAttack_table_list)
    normalAttack_Stat_Table = []
    for thisList in normalAttack_table_list:
        if len(thisList[0]) > 1:
            i = 1
            this_stat_dict = {}
            this_stat_table_dict = {}
            this_stat_dict['Name'] = thisList[0]
            while i < len(thisList):
                this_stat_table_dict[normalAttack_table_list[0][i]] = thisList[i]
                i += 1
            this_stat_dict['Values'] = this_stat_table_dict
            normalAttack_Stat_Table.append(this_stat_dict)
    normalAttack['Name'] = normalAttack_name
    normalAttack['Source'] = normalAttack_imageURL
    normalAttack['Description'] = str(normalAttack_desc)
    normalAttack['Table'] = normalAttack_Stat_Table
    # print(normalAttack)
    ### 生成Json
    normalAttack_Json = json.dumps(normalAttack, ensure_ascii=False, indent=4, separators=(',', ':'))
    normalAttack_Json = normalAttack
    #print(normalAttack_Json)

    ## E技能
    #print("=" * 20 + "\nE技能")
    skillE = {}
    ### 介绍
    skillE_area = normalAttack_table_area.find_next_sibling()
    skillE_info = skillE_area.find_all('tr')
    skillE_imageURL = URL_Prefix + skillE_info[0].find('img', {'class': 'itempic'})['data-src']
    skillE_imageURL = skillE_imageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
    # print("imageURL: " + skillE_imageURL)
    skillE_name = skillE_info[0].find('a', href=re.compile('/db/skill/')).text
    # print("attack_name: " + str(skillE_name))
    skillE_desc = skillE_info[1].find('div', {'class': 'skill_desc_layout'}).text.replace(" ", "\n")
    # print("normalAttack_desc: " + str(skillE_desc))
    ### 表格
    skillE_table_list = []
    skillE_table_area = skillE_area.find_next_sibling()
    skillE_table = skillE_table_area.find_all('tr')
    for eachLine in skillE_table:
        this_line_list = []
        all_columns = eachLine.find_all('td')
        for each_column in all_columns:
            this_item = each_column.text
            this_line_list.append(this_item)
        skillE_table_list.append(this_line_list)
    # for item in skillE_table_list:
    # print(item)

    ## 生成字典
    skillE_Stat_Table = []
    for thisList in skillE_table_list:
        if len(thisList[0]) > 1:
            i = 1
            this_stat_dict = {}
            this_stat_table_dict = {}
            this_stat_dict['Name'] = thisList[0]
            while i < len(thisList):
                this_stat_table_dict[skillE_table_list[0][i]] = thisList[i]
                i += 1
            this_stat_dict['Values'] = this_stat_table_dict
            skillE_Stat_Table.append(this_stat_dict)
    skillE['Name'] = skillE_name
    skillE['Source'] = skillE_imageURL
    skillE['Description'] = str(skillE_desc)
    skillE['Table'] = skillE_Stat_Table
    ### 生成Json
    skillE_Json = json.dumps(skillE, ensure_ascii=False, indent=4, separators=(',', ':'))
    skillE_Json = skillE
    #print(skillE_Json)

    ## Q技能
    #print("=" * 20 + "\nQ技能")
    skillQ = {}
    load_another_talentQ = False  # 针对神里绫华和莫娜的专属修复
    ### 介绍
    skillQ_area = skillE_table_area.find_next_sibling()
    skillQ_info = skillQ_area.find_all('tr')
    skillQ_imageURL = URL_Prefix + skillQ_info[0].find('img', {'class': 'itempic'})['data-src']
    skillQ_imageURL = skillQ_imageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
    # print("imageURL: " + skillQ_imageURL)
    skillQ_name = skillQ_info[0].find('a', href=re.compile('/db/skill/')).text
    # print("attack_name: " + str(skillQ_name))
    skillQ_desc = skillQ_info[1].find('div', {'class': 'skill_desc_layout'}).text.replace(" ", "\n")
    # print("normalAttack_desc: " + str(skillQ_desc))
    ### 表格
    skillQ_table_list = []
    skillQ_table_area = skillQ_area.find_next_sibling()
    skillQ_table = skillQ_table_area.find_all('tr')
    for eachLine in skillQ_table:
        this_line_list = []
        all_columns = eachLine.find_all('td')
        for each_column in all_columns:
            this_item = each_column.text
            this_line_list.append(this_item)
        skillQ_table_list.append(this_line_list)
    ## 生成字典
    skillQ_Stat_Table = []
    for thisList in skillQ_table_list:
        if len(thisList[0]) > 1:
            i = 1
            this_stat_dict = {}
            this_stat_table_dict = {}
            this_stat_dict['Name'] = thisList[0]
            while i < len(skillQ_table_list[0]):
                try:
                    this_stat_table_dict[skillQ_table_list[0][i]] = thisList[i]
                except IndexError:
                    # 神里绫华/莫娜 专属修复
                    this_stat_table_dict[skillQ_table_list[0][i]] = ""
                    load_another_talentQ = True
                i += 1
            this_stat_dict['Values'] = this_stat_table_dict
            skillQ_Stat_Table.append(this_stat_dict)
    skillQ['Name'] = skillQ_name
    skillQ['Source'] = skillQ_imageURL
    skillQ['Description'] = str(skillQ_desc)
    skillQ['Table'] = skillQ_Stat_Table
    ### 生成Json
    skillQ_Json = json.dumps(skillQ, ensure_ascii=False, indent=4, separators=(',', ':'))
    skillQ_Json = skillQ
    #print(skillQ_Json)

    if load_another_talentQ:
        ## Q2技能 (神里绫华和莫娜的大招)
        #print("=" * 20 + "\nQ技能")
        skillQ2 = {}
        ### 介绍
        skillQ2_area = skillQ_table_area.find_next_sibling()
        skillQ2_info = skillQ2_area.find_all('tr')
        skillQ2_imageURL = URL_Prefix + skillQ2_info[0].find('img', {'class': 'itempic'})['data-src']
        skillQ2_imageURL = skillQ2_imageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
        # print("imageURL: " + skillQ2_imageURL)
        skillQ2_name = skillQ2_info[0].find('a', href=re.compile('/db/skill/')).text
        # print("attack_name: " + str(skillQ2_name))
        skillQ2_desc = skillQ2_info[1].find('div', {'class': 'skill_desc_layout'}).text.replace(" ", "\n")
        # print("normalAttack_desc: " + str(skillQ2_desc))
        ### 表格
        skillQ2_table_list = []
        skillQ2_table_area = skillQ2_area.find_next_sibling()
        skillQ2_table = skillQ2_table_area.find_all('tr')
        for eachLine in skillQ2_table:
            this_line_list = []
            all_columns = eachLine.find_all('td')
            for each_column in all_columns:
                this_item = each_column.text
                this_line_list.append(this_item)
            skillQ2_table_list.append(this_line_list)
        ## 生成字典
        skillQ2_Stat_Table = []
        for thisList in skillQ2_table_list:
            if len(thisList[0]) > 1:
                i = 1
                this_stat_dict = {}
                this_stat_table_dict = {}
                this_stat_dict['Name'] = thisList[0]
                while i < len(skillQ2_table_list[0]):
                    this_stat_table_dict[skillQ2_table_list[0][i]] = thisList[i]
                    i += 1
                this_stat_dict['Values'] = this_stat_table_dict
                skillQ2_Stat_Table.append(this_stat_dict)
        skillQ2['Name'] = skillQ2_name
        skillQ2['Source'] = skillQ2_imageURL
        skillQ2['Description'] = str(skillQ2_desc)
        skillQ2['Table'] = skillQ2_Stat_Table
        ### 生成Json
        skillQ2_Json = json.dumps(skillQ2, ensure_ascii=False, indent=4, separators=(',', ':'))
        skillQ2_Json = skillQ2
        #print(skillQ2_Json)

    ## 天赋升级材料
    #print("=" * 20 + "\n天赋升级材料")
    TelentMaterials_list = []
    TelentMaterials_area = main_content.find('span',
                                             string='Talent Ascension Materials (All 3 Talents lvl 10)').find_next_sibling()
    TelentMaterials_area_list = TelentMaterials_area.find_all('div', {'class': 'nowrap_rew_cont'})
    for item in TelentMaterials_area_list:
        itemImageURL = URL_Prefix + item.find('img', {'class': 'itempic'})['data-src']
        itemImageURL = itemImageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
        itemRequiredNumber = item.find('div', {'class': 'itemstarcontbg_smol'}).text
        thisItemList = [itemImageURL, itemRequiredNumber]
        TelentMaterials_list.append(thisItemList)
    #print(TelentMaterials_list)

    ## 被动天赋
    if load_another_talentQ:
        PassiveTalentsList = [skillQ]
    else:
        PassiveTalentsList = []
    PassiveTalentsArea = main_content.find('span', string='Passive Talents').find_next_sibling()
    AllPassiveTalentsElements = PassiveTalentsArea.find_all('tr')
    i = 0
    while i < len(AllPassiveTalentsElements):
        thisPassiveTalents = {}
        if (i + 1) % 2 != 0:
            # print("This is a start of a constellation")
            this_line = AllPassiveTalentsElements[i]
            imageURL = URL_Prefix + this_line.find_all('img', {'class': 'itempic'})[-1]['data-src']
            imageURL = imageURL.replace("https://genshin.honeyhunterworld.com//", "https://genshin.honeyhunterworld.com/")
            #print("imgURL: " + str(imageURL))
            PassiveTalentsName = this_line.find_all('a', href=re.compile("/db/skill"))[-1].text
            #print("PassiveTalentsName: " + PassiveTalentsName)
            this_line = AllPassiveTalentsElements[i + 1]
            PassiveTalentsDesc = this_line.find('div', {'class': 'skill_desc_layout'}).text
            #print("PassiveTalentsDesc: " + PassiveTalentsDesc)

            # Add to list
            thisPassiveTalents['Source'] = imageURL
            thisPassiveTalents['Name'] = PassiveTalentsName
            thisPassiveTalents['Description'] = PassiveTalentsDesc
            PassiveTalentsList.append(thisPassiveTalents)
            i += 2
    PassiveTalents_Json = json.dumps(PassiveTalentsList, ensure_ascii=False, indent=4, separators=(',', ':'))
    PassiveTalents_Json = PassiveTalentsList

    if load_another_talentQ:
        return [charTableJson, Constellations_Json, normalAttack_Json,
                skillE_Json, skillQ2_Json, PassiveTalents_Json, CharTitle, charAstrolabeName, charDescription]
    else:
        return [charTableJson, Constellations_Json, normalAttack_Json,
                skillE_Json, skillQ_Json, PassiveTalents_Json, CharTitle, charAstrolabeName, charDescription]
    '''
    返回内容： 角色基本数值Dict，命之座Dict，基础攻击数值Dict
            E技能数值Dict，Q技能数值Dict，角色标题Str，命之座名称Str，角色介绍Str
    '''


if __name__ == "__main__":
    '''
    # Test demo
    # getCharInfo("https://genshin.honeyhunterworld.com/db/char/amber/?lang=CHS")
    f = open('characters.json', encoding='utf-8')
    data = json.load(f)
    testChar = data[0]
    print(testChar)
    print(type(testChar))
    thisURL = "https://genshin.honeyhunterworld.com/db/char/" + testChar['Key'].lower() + "/?lang=CHS"
    new_data_list = getCharInfo(thisURL)
    print("-"*20)
    print(type(new_data_list[1]))
    testChar["CharStat"] = new_data_list[0]
    testChar["Constellations"] = new_data_list[1]
    testChar["NormalAttack"] = new_data_list[2]
    testChar["TalentE"] = new_data_list[3]
    testChar["TalentQ"] = new_data_list[4]
    new_json = json.dumps(testChar, ensure_ascii=False, indent=4, separators=(',', ':'))
    f_output = open("demo.json", mode="a", encoding='utf-8')
    f_output.write(new_json)
    f_output.close()
    '''


    f = open('characters.json', encoding='utf-8')
    data = json.load(f)
    newFileList = []
    for character in data:
        try:
            print("加载数据：" + character['Key'])
            keyName = character['Key'].lower()
            if keyName == "yanfei":
                keyName = "feiyan"
            if keyName == "raidenshogun":
                keyName = "shougun"
            thisURL = "https://genshin.honeyhunterworld.com/db/char/" + keyName + "/?lang=CHS"
            returned_list = getCharInfo(thisURL)
            character["CharStat"] = returned_list[0]
            character["Constellations"] = returned_list[1]
            character["NormalAttack"] = returned_list[2]
            character["TalentE"] = returned_list[3]
            character["TalentQ"] = returned_list[4]
            character["PassiveTalents"] = returned_list[5]
            character["Title"] = returned_list[6]
            character["AstrolabeName"] = returned_list[7]
            character["Description"] = returned_list[8]
            print(character['Key'] + "任务完成")
            newFileList.append(character)
            time.sleep(0)
        except:
            print("Error when working for " + character['Key'])
    newFileList = json.dumps(newFileList, ensure_ascii=False, indent=4, separators=(',', ':'))
    f_output = open("result.json", mode="a", encoding='utf-8')
    f_output.write(newFileList)
    f_output.close()




