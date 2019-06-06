import re
import random
import pandas as pd

random.seed(1213)

pm_train = "data/PM/train.txt"
pm_dev = "data/PM/dev.txt"
pm_test9870_ec = "data/PM/candidate_predicate_bert_9870_ec.txt"
pm_infer9870_all = "data/PM/candidate_predicate_bert_9870_all.txt"

xq_train = "data/XQ/candidate_entity_train.txt"
xq_dev = "data/XQ/candidate_entity_dev.txt"
xq_test9870_mc= "data/XQ/candidate_entity_test_bert_9870_mc.txt"
xq_infer9870 = "data/XQ/candidate_entity_test_bert_9870.txt"


def pm_process_train_dev(infile, outfile, with_mention=True):
    """
    <question id=2> | 《 犯 罪 学 》 | 的 isbn 码 是 什 么
    <answer id=2>   9787300088082
    <triple id=2>   《 犯 罪 学 》 ( 曹 立 群 与 任 昕 主 编 )   ISBN    9787300088082
    <candidate id=2>    别 名 中 文 名   作 者 类 别 价 格 语 种 出 版 社   页 数 开 本 出 版 时 间 简 介 装 帧 其 他

    :param infile: raw file
    :param outfile: csv file for train/dev
    :param with_mention: whether replace the mention in question with a special token "entity"
    """
    p = "id=(.*?)>"  # id pattern
    fw = open(outfile, "w")
    with open(infile) as f:
        i = 0
        new_line = ""
        output_line = ""
        relation = ""
        for line in f:
            i += 1
            if i % 5 == 1:
                # line: <question id=2> | 《 犯 罪 学 》 | 的 isbn 码 是 什 么
                line = line.strip().lower().split("\t")
                res = re.search(p, line[0])
                idx = res.group(1)
                question = line[1]
                question = question.split("|")
                if len(question) == 3:
                    if not with_mention:  # TODO: replace the mention in question with a special token "entity"
                        question[1] = "entity"
                    question = "".join(question).strip()
                    question = re.sub(r"\s+", r" ", question)
                new_line += str(question) + "\t"
                # new_line: 《 犯 罪 学 》 的 isbn 码 是 什 么\t
                # new_line: entity 的 isbn 码 是 什 么\t     (with_mention=False)
            elif i % 5 == 2:
                pass
                # <answer id=2>   9787300088082
            elif i % 5 == 3:
                # <triple id=2>   《 犯 罪 学 》 ( 曹 立 群 与 任 昕 主 编 )   ISBN    9787300088082
                line = line.strip().lower().split("\t")
                try:
                    relation = line[2]
                    output_line = str(idx) + '-0' + '\t' + new_line + str(relation) + "\t" + "1" + "\n"
                except IndexError:
                    print("%s: There is no golden relation in question." % idx)
                    output_line = ""
                fw.write(output_line)
                # output_line: 2-1\t《 犯 罪 学 》 的 isbn 码 是 什 么\tISBN\t1\n
                # output_line: 2-1\tentity 的 isbn 码 是 什 么\tISBN\t1\n      (with_mention=False)
            elif i % 5 == 4:
                # line: <candidate id=2>    别 名 中 文 名   作 者 类 别 价 格 语 种 出 版 社   页 数 开 本 出 版 时 间 简 介 装 帧 其 他
                line = line.strip().lower().split("\t")
                outputs = []
                index = 0
                for c in line[1:]:
                    if c != relation:
                        index += 1
                        outputs.append(str(idx) + '-' + str(index) + '\t' + new_line + str(c) + "\t" + "0" + "\n")
                    else:
                        print("%s: Golden relation appears in candidate predicates." % idx)
                fw.writelines(outputs)
                # outputs:
                #   2-1\t《 犯 罪 学 》 的 isbn 码 是 什 么\t别 名\t0\n
                #   2-1\tentity 的 isbn 码 是 什 么\t别 名\t0\n      (with_mention=False)
                #   ......
            else:
                new_line = ""
                output_line = ""
                continue


def pm_process_test(infile, outfile, with_mention=True):
    """
    <question id=1-1>   你 知 道 | 计 算 机 应 用 基 础 | 这 本 书 的 作 者 是 谁 吗 ？
    <triple id=1-1> 计 算 机 应 用 基 础   作 者 刘晓斌、魏智荣、刘庆生
    <candidate id=1-1>  页 数 别 名 中 文 名   定 价 isbn    装 帧 出 版 社   原 作 者   开 本 字 数 类 别 出 版 时 间

    :param infile: raw file
    :param outfile: csv file for test
    :param with_mention:  whether replace the mention in question with a special token "entity"
    """
    # id pattern
    p = "id=(.*?)>"
    fw = open(outfile, "w")
    with open(infile) as f:
        i = 0
        new_line = ""
        output_line = ""
        relation = ""
        for line in f:
            i += 1
            if i % 4 == 1:
                # line: <question id=1-1>   你 知 道 | 计 算 机 应 用 基 础 | 这 本 书 的 作 者 是 谁 吗 ？
                line = line.strip().lower().split("\t")
                res = re.search(p, line[0])
                idx = res.group(1)
                question = line[1]
                question = question.split("|")
                if len(question) == 3:
                    if not with_mention:   # TODO: replace the mention in question with a special token "entity"
                        question[1] = "entity"
                    question = "".join(question).strip()
                    question = re.sub(r"\s+", r" ", question)
                new_line += str(question) + "\t"
            elif i % 4 == 2:
                # <triple id=1-1> 计 算 机 应 用 基 础   作 者 刘晓斌、魏智荣、刘庆生
                line = line.strip().lower().split("\t")
                try:
                    relation = line[2]
                    output_line = str(idx) + '\t' + new_line + str(relation) + "\t" + "1" + "\n"
                except IndexError:
                    print("%s: There is no golden relation in question." % idx)
                    output_line = ""
                fw.write(output_line)

            elif i % 4 == 3:
                # <candidate id=1-1>  页 数 别 名 中 文 名   定 价 isbn    装 帧 出 版 社   原 作 者   开 本 字 数 类 别 出 版 时 间
                line = line.strip().lower().split("\t")
                outputs = []
                for c in line[1:]:
                    if c != relation:
                        outputs.append(str(idx) + '\t' + new_line + str(c) + "\t" + "0" + "\n")
                    else:
                        print("%s: Golden relation appears in candidate predicates." % idx)
                fw.writelines(outputs)
            else:
                new_line = ""
                output_line = ""
                continue


def pm_process_infer(infile, outfile, with_mention=True):
    """
    <question id=1-1>   你 知 道 | 计 算 机 应 用 基 础 | 这 本 书 的 作 者 是 谁 吗 ？
    <triple id=1-1> 计 算 机 应 用 基 础   作 者 刘晓斌、魏智荣、刘庆生
    <candidate id=1-1>  出 版 时 间 isbn    定 价 开 本 别 名 字 数 作 者 丛 书 名   页 数 装 帧 书 名
    <e_score id=1-1>    计 算 机 应 用 基 础 ( 含 职 业 模 块 ) 0.044469457000000004

    :param infile: raw file
    :param outfile: csv file for infer
    :param with_mention: whether replace the mention in question with a special token "entity"
    """
    p = "id=(.*?)>"     # id pattern
    fw = open(outfile, "w")
    with open(infile) as f:
        i = 0
        new_line = ""
        for line in f:
            i += 1
            if i % 5 == 1:
                # line: <question id=1-1>   你 知 道 | 计 算 机 应 用 基 础 | 这 本 书 的 作 者 是 谁 吗 ？
                line = line.strip().lower().split("\t")
                res = re.search(p, line[0])
                idx = res.group(1)
                question = line[1]
                question = question.split("|")
                if len(question) == 3:
                    if not with_mention:
                        question[1] = "entity"
                    question = "".join(question).strip()
                    question = re.sub(r"\s+", r" ", question)
                new_line += str(question) + "\t"
                # new_line: 你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t
            elif i % 5 == 2:
                pass
            elif i % 5 == 3:
                # line: <candidate id=1-1>  出 版 时 间 isbn    定 价 开 本 别 名 字 数 作 者 丛 书 名   页 数 装 帧 书 名
                line = line.strip().lower().split("\t")
                outputs = [str(idx) + '\t' + new_line + str(c) + "\n" for i, c in enumerate(line[1:])]
                fw.writelines(outputs)
                # outputs:
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t出 版 时 间\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\tisbn\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t定 价\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t开 本\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t别 名\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t字 数\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t作 者\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t丛 书 名\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t页 数\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t装 帧\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t书 名\n
            elif i % 5 == 4:
                pass
            else:
                new_line = ""
                continue


def xq_process_train_dev_test(infile, outfile):
    """
    <question id=2-1>   | 《 犯 罪 学 》 | 的 isbn 码 是 什 么
    <triple id=2-1> 《 犯 罪 学 》 ( 曹 立 群 与 任 昕 主 编 )   isbn    9787300088082
    <candidate id=2-1>  《 犯 罪 学 》 ( 许 章 润 主 编 ) 《 犯 罪 学 》 ( 康 树 华 与 张 小 虎 主 编 ) 《 犯 罪 学 》 ( 道 尔 戈 娃 主 编 )

    :param infile: raw file
    :param outfile: csv file for train/dev
    """
    p = "id=(.*?)>"  # id pattern
    fw = open(outfile, "w")
    with open(infile) as f:
        i = 0
        new_line = ""
        output_line = ""
        relation = ""
        for line in f:
            i += 1
            if i % 4 == 1:
                # line: <question id=2-1>   | 《 犯 罪 学 》 | 的 isbn 码 是 什 么
                line = line.strip().lower().split("\t")
                res = re.search(p, line[0])
                idx = res.group(1)
                question = line[1]
                question = "".join(question.split("|")).strip()
                question = re.sub(r"\s+", r" ", question)
                new_line += str(question) + "\t"
                # new_line: 《 犯 罪 学 》 的 isbn 码 是 什 么\t
            elif i % 4 == 2:
                # line: <triple id=2-1> 《 犯 罪 学 》 ( 曹 立 群 与 任 昕 主 编 )   isbn    9787300088082
                line = line.strip().lower().split("\t")
                try:
                    entity = line[1]
                    output_line = str(idx) + '\t' + new_line + str(entity) + "\t" + "1" + "\n"
                except IndexError:
                    print("%s: There is no golden entity in question." % idx)
                    output_line = ""
                # output_line = 2-1\t《 犯 罪 学 》 的 isbn 码 是 什 么\t《 犯 罪 学 》 ( 曹 立 群 与 任 昕 主 编 )\t1\n
                fw.write(output_line)
            elif i % 4 == 3:
                # line: <candidate id=2-1>  《 犯 罪 学 》 ( 许 章 润 主 编 ) 《 犯 罪 学 》 ( 康 树 华 与 张 小 虎 主 编 ) 《 犯 罪 学 》 ( 道 尔 戈 娃 主 编 )
                line = line.strip().lower().split("\t")
                outputs = []
                for c in line[1:]:
                    if c != entity:
                        outputs.append(str(idx) + '\t' + new_line + str(c) + "\t" + "0" + "\n")
                    else:
                        print("%s: Golden entity appears in candidate entities." % idx)
                # outputs:
                #   2-1\t《 犯 罪 学 》 的 isbn 码 是 什 么\t《 犯 罪 学 》 ( 许 章 润 主 编 )\t0\n
                #   2-1\t《 犯 罪 学 》 的 isbn 码 是 什 么\t《 犯 罪 学 》 ( 康 树 华 与 张 小 虎 主 编 )\t0\n
                #   2-1\t《 犯 罪 学 》 的 isbn 码 是 什 么\t《 犯 罪 学 》 ( 道 尔 戈 娃 主 编 )\t0\n
                fw.writelines(outputs)
            else:
                new_line = ""
                output_line = ""
                continue


def xq_process_infer(infile, outfile):
    """
    <question id=1-1>   你 知 道 | 计 算 机 应 用 基 础 | 这 本 书 的 作 者 是 谁 吗 ？
    <triple id=1-1> 计 算 机 应 用 基 础   作 者 刘晓斌、魏智荣、刘庆生
    <candidate id=1-1>  计 算 机 应 用 基 础   计 算 机 应 用 基 础 ( 2010 年 中 国 铁 道 出 版 社 出 版 图 书 )  计 算 机 应 用 基 础 ( 中 国 电 力 出 版 社 出 版 书 籍 ) 计 算 机 应 用 基 础 ( 2010 年 8 月 中 国 铁 道 出 版 社 出 版 图 书 )  计 算 机 应 用 基 础 ( 电 子 工 业 出 版 社 出 版 图 书 ) 

    :param infile: raw file
    :param outfile: csv file for infer
    """
    p = "id=(.*?)>"     # id pattern
    fw = open(outfile, "w")
    with open(infile) as f:
        i = 0
        new_line = ""
        for line in f:
            i += 1
            if i % 4 == 1:
                # line: <question id=1-1>   你 知 道 | 计 算 机 应 用 基 础 | 这 本 书 的 作 者 是 谁 吗 ？
                line = line.strip().lower().split("\t")
                res = re.search(p, line[0])
                idx = res.group(1)
                question = line[1]
                question = question.split("|")
                if len(question) == 3:
                    question = "".join(question).strip()
                    question = re.sub(r"\s+", r" ", question)
                new_line += str(question) + "\t"
                # new_line: 你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t
            elif i % 4 == 2:
                pass
            elif i % 4 == 3:
                # <candidate id=1-1>  计 算 机 应 用 基 础   计 算 机 应 用 基 础 ( 2010 年 中 国 铁 道 出 版 社 出 版 图 书 )  计 算 机 应 用 基 础 ( 中 国 电 力 出 版 社 出 版 书 籍 ) 计 算 机 应 用 基 础 ( 2010 年 8 月 中 国 铁 道 出 版 社 出 版 图 书 )  计 算 机 应 用 基 础 ( 电 子 工 业 出 版 社 出 版 图 书 ) 
                line = line.strip().lower().split("\t")
                outputs = [str(idx) + '\t' + new_line + str(c) + "\n" for i, c in enumerate(line[1:])]
                fw.writelines(outputs)
                # outputs: 
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t计 算 机 应 用 基 础\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t计 算 机 应 用 基 础 ( 2010 年 中 国 铁 道 出 版 社 出 版 图 书 )\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t计 算 机 应 用 基 础 ( 中 国 电 力 出 版 社 出 版 书 籍 )\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t计 算 机 应 用 基 础 ( 2010 年 8 月 中 国 铁 道 出 版 社 出 版 图 书 )\n
                #   1-1\t你 知 道 计 算 机 应 用 基 础 这 本 书 的 作 者 是 谁 吗 ？\t计 算 机 应 用 基 础 ( 电 子 工 业 出 版 社 出 版 图 书 )\n
                #   ......
            else:
                new_line = ""
                continue


if __name__ == "__main__":
    # pm data
    pm_process_train_dev(pm_train, "data/PM/train.csv", with_mention=False)
    train_df = pd.read_csv("data/PM/train.csv", header=None, sep="\t", quoting=3)
    print(train_df.head(100))
    train_df.to_csv("data/PM/train.csv", header=False, index=False, sep="\t")

    pm_process_train_dev(pm_dev, "data/PM/dev.csv", with_mention=False)
    dev_df = pd.read_csv("data/PM/dev.csv", header=None, sep="\t", quoting=3)
    print(dev_df.head(100))
    dev_df.to_csv("data/PM/dev.csv", header=False, index=False, sep="\t")

    pm_process_test(pm_test9870_ec, "data/PM/test9870.csv", with_mention=False)
    test_df = pd.read_csv("data/PM/test9870.csv", header=None, sep="\t", quoting=3)
    print(test_df.head(100))
    test_df.to_csv("data/PM/test9870.csv", header=False, index=False, sep="\t")

    pm_process_infer(pm_infer9870_all, "data/PM/infer9870_all.csv", with_mention=False)
    infer_df = pd.read_csv("data/PM/infer9870_all.csv", header=None, sep="\t", quoting=3)
    print(infer_df.head(100))
    infer_df.to_csv("data/PM/infer9870_all.csv", header=False, index=False, sep="\t")

    # pm data with mention
    pm_process_train_dev(pm_train, "data/PM/train_with_mention.csv", with_mention=True)
    train_df = pd.read_csv("data/PM/train_with_mention.csv", header=None, sep="\t", quoting=3)
    print(train_df.head(100))
    train_df.to_csv("data/PM/train_with_mention.csv", header=False, index=False, sep="\t")

    pm_process_train_dev(pm_dev, "data/PM/dev_with_mention.csv", with_mention=True)
    dev_df = pd.read_csv("data/PM/dev_with_mention.csv", header=None, sep="\t", quoting=3)
    print(dev_df.head(100))
    dev_df.to_csv("data/PM/dev_with_mention.csv", header=False, index=False, sep="\t")

    pm_process_test(pm_test9870_ec, "data/PM/test9870_with_mention.csv", with_mention=True)
    test_df = pd.read_csv("data/PM/test9870_with_mention.csv", header=None, sep="\t", quoting=3)
    print(test_df.head(100))
    test_df.to_csv("data/PM/test9870_with_mention.csv", header=False, index=False, sep="\t")

    pm_process_infer(pm_infer9870_all, "data/PM/infer9870_all_with_mention.csv", with_mention=True)
    infer_df = pd.read_csv("data/PM/infer9870_all_with_mention.csv", header=None, sep="\t", quoting=3)
    print(infer_df.head(100))
    infer_df.to_csv("data/PM/infer9870_all_with_mention.csv", header=False, index=False, sep="\t")

    # xq data
    xq_process_train_dev_test(xq_train, "data/XQ/train.csv")
    train_df = pd.read_csv("data/XQ/train.csv", header=None, sep="\t", quoting=3)
    print(train_df.head(100))
    train_df.columns = ["id", "sep1", "sep2", "label"]
    train_df.to_csv("data/XQ/train.csv", header=False, index=False, sep="\t")

    xq_process_train_dev_test(xq_dev, "data/XQ/dev.csv")
    dev_df = pd.read_csv("data/XQ/dev.csv", header=None, sep="\t", quoting=3)
    print(dev_df.head(100))
    dev_df.to_csv("data/XQ/dev.csv", header=False, index=False, sep="\t")

    xq_process_train_dev_test(xq_test9870_mc, "data/XQ/test9870.csv")
    test_df = pd.read_csv("data/XQ/test9870.csv", header=None, sep="\t", quoting=3)
    print(test_df.head(100))
    test_df.to_csv("data/XQ/test9870.csv", header=False, index=False, sep="\t")

    xq_process_infer(xq_infer9870, "data/XQ/infer9870.csv")
    infer_df = pd.read_csv("data/XQ/infer9870.csv", header=None, sep="\t", quoting=3)
    print(infer_df.head(100))
    infer_df.to_csv("data/XQ/infer9870.csv", header=False, index=False, sep="\t")

    print("Done!")
