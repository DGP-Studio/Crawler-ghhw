import json

if __name__ == "__main__":
    print("请将本脚本置于 characters.json 文件同目录下并启动")
    print("本脚本用于修复烟绯Q技能数据列表错误")
    input("按回车开始运行...")
    f = open('characters.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    for character in data:
        if character['Key'] == "feiyan":
            stat = character["TalentQ"]["Table"]
            #print(stat)
            """
            内鬼网的原始顺序
            stat[0]: 技能伤害 --> 不变
            stat[1]: 丹火印赋予间隔 --> Values 更改为 stat[2]['Values']
            stat[2]: 重击伤害提升 --> Values 更改为 stat[3]['Values']
            stat[3]: 持续时间  --> Values 更改为 stat[4]['Values']
            stat[4]: 冷却时间  --> Values 更改为 stat[5]['Values']
            stat[5]: 元素能量  --> Values 全部改为 80
            """
            character["TalentQ"]["Table"][1]['Values'] = stat[2]['Values'].copy()
            character["TalentQ"]["Table"][2]['Values'] = stat[3]['Values'].copy()
            character["TalentQ"]["Table"][3]['Values'] = stat[4]['Values'].copy()
            character["TalentQ"]["Table"][4]['Values'] = stat[5]['Values'].copy()
            for key in character["TalentQ"]["Table"][5]['Values']:
                character["TalentQ"]["Table"][5]['Values'][key] = "80"

    newFileList = json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':'))
    f_output = open("characters-YanfeiFixed.json", mode="a", encoding='utf-8')
    f_output.write(newFileList)
    f_output.close()
    print("脚本执行完成")

