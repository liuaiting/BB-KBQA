from __future__ import division

import re
from sklearn.metrics.classification import f1_score, accuracy_score, precision_score, recall_score
import pandas as pd

xq_raw_file = "data/XQ/test9870.csv"
xq_result_file = "xq_output/test_results_9870_mc.tsv"

pm_raw_file = "data/PM/test9870.csv"
pm_result_file = "pm_output/test_results_9870_ec.tsv"

pm_with_mention_raw_file = "data/PM/test9870_with_mention.csv"
pm_with_mention_result_file = "pm_output_with_mention/test_results_9870_ec_with_mention.tsv"


def func(a, b):
    if a >= b:
        return 1
    else:
        return 0


def myaccuracy(raw_file, result_file):
    df = pd.read_csv(result_file, sep='\t', header=None, names=['pred_0', 'pred_1'])
    test_df = pd.read_csv(raw_file, sep='\t', header=None, names=['idx', 'question', 'relation', 'label'])

    df["pred"] = df.apply(lambda row: func(row["pred_1"], row["pred_0"]), axis=1)
    f1 = f1_score(y_true=test_df.label, y_pred=df.pred)
    acc = accuracy_score(y_true=test_df.label, y_pred=df.pred)
    p = precision_score(y_true=test_df.label, y_pred=df.pred)
    r = recall_score(y_true=test_df.label, y_pred=df.pred)
    print("accuracy: ", acc)
    print("precision: ", p)
    print("recall: ", r)
    print("f1: ", f1)

    # df['idx'] = test_df.idx.map(lambda x: x.split('-')[0])
    df["idx"] = test_df.idx
    df["group_sort"] = df["pred_1"].groupby(df["idx"]).rank(ascending=0, method="dense")
    df["candidate"] = test_df.relation

    # test_df['idx'] = test_df.idx.map(lambda x: x.split('-')[0])

    df.drop_duplicates(subset=['idx', 'group_sort'], keep='first', inplace=True)
    true_relation = test_df.loc[test_df["label"] == 1]
    pred_relation = df.loc[(df["group_sort"] == 1.0)]

    # print(pred_relation.tail())
    # print(true_relation.tail())
    new_df = pd.merge(true_relation, pred_relation, how="inner")
    new_df["correct"] = new_df.apply(lambda row: row["relation"] == row["candidate"], axis=1)
    c = new_df.loc[new_df["correct"] == True]
    correct = c.idx.count()
    total = new_df.idx.count()
    print("my_accuracy: {}, {}/{}".format(correct/total, correct, total))


# myaccuracy(xq_raw_file, xq_result_file)
# myaccuracy(pm_raw_file, pm_result_file)
# myaccuracy(pm_with_mention_raw_file, pm_with_mention_result_file)


def process_infer_result(pred_file, infer_file, id_pred_file):
    df = pd.read_csv(pred_file, sep='\t', header=None, names=['pred_0', 'pred_1'])
    infer_df = pd.read_csv(infer_file, sep='\t', header=None, names=['idx', 'question', 'relation', 'label'])
    df["idx"] = infer_df.idx
    print(df.head())
    df.to_csv(id_pred_file, index=False, header=False, sep="\t", columns=["idx", "pred_1"])


def column4_to_row(id_pred_file, raw_file, result_file):
    f = open(id_pred_file, "r")
    dic = {}
    for line in f:
        l = line.split()
        idx = l[0]
        score = l[1]
        if not dic.get(idx):
            dic[idx] = str(score)
        else:
            dic[idx] += "\t" + str(score)
    f.close()

    p = "id=(.*?)>"
    fi = open(raw_file, "r")
    fw = open(result_file, "w")
    i = 0
    res = ""
    idx = ""

    for line in fi:
        i += 1
        if i % 4 == 1:
            id_find = re.search(p, line)
            idx = id_find.group(1)
            res += line
        elif i % 4 == 2:
            res += line
        elif i % 4 == 3:
            res += line
        else:
            if dic.get(idx):
                res += "<r_score id={}>\t{}\n".format(str(idx), dic[idx])
            else:
                res += "<r_score id={}>\t{}\n".format(str(idx), "")
            fw.write(res + "\n")
            res = ""

    fi.close()
    fw.close()


def column5_to_row(id_pred_file, raw_file, result_file):
    f = open(id_pred_file, "r")
    dic = {}
    for line in f:
        l = line.split()
        idx = l[0]
        score = l[1]
        if not dic.get(idx):
            dic[idx] = str(score)
        else:
            dic[idx] += "\t" + str(score)
    f.close()

    p = "id=(.*?)>"
    fi = open(raw_file, "r")
    fw = open(result_file, "w")
    i = 0
    res = ""
    idx = ""

    for line in fi:
        i += 1
        if i % 5 == 1:
            id_find = re.search(p, line)
            idx = id_find.group(1)
            res += line
        elif i % 5 == 2:
            res += line
        elif i % 5 == 3:
            res += line
        elif i % 5 == 4:
            res += line
        else:
            if dic.get(idx):
                res += "<r_score id={}>\t{}\n".format(str(idx), dic[idx])
            else:
                res += "<r_score id={}>\t{}\n".format(str(idx), "")
            fw.write(res + "\n")
            res = ""

    fi.close()
    fw.close()


process_infer_result("pm_output/test_results_9870_ec.tsv", "data/PM/test9870.csv", "result/id_test9870_ec.csv")
column4_to_row("result/id_test9870_ec.csv", "data/PM/candidate_predicate_bert_9870_ec.txt", "result/pm_result_9870_ec")

# process_infer_result("pm_output_with_mention/test_results_9870_ec_with_mention.tsv", "data/PM/test9870_with_mention.csv", "result/id_test9870_ec_with_mention.csv")
# column4_to_row("result/id_test9870_ec_with_mention.csv", "data/PM/candidate_predicate_bert_9870_ec.txt", "result/pm_result_9870_ec_with_mention")

# process_infer_result("pm_output/test_results_9870_all.tsv", "data/PM/infer9870_all.csv", "result/id_infer9870_all.csv")
# column5_to_row("result/id_infer9870_all.csv", "data/PM/candidate_predicate_bert_9870_all.txt", "result/pm_result_9870_all")

# process_infer_result("pm_output_with_mention/test_results_9870_all_with_mention.tsv", "data/PM/infer9870_all_with_mention.csv", "result/id_test9870_all_with_mention.csv")
# column5_to_row("result/id_test9870_all_with_mention.csv", "data/PM/candidate_predicate_bert_9870_all.txt", "result/pm_result_9870_all_with_mention")

# process_infer_result("xq_output/test_results_9870_mc.tsv", "data/XQ/test9870.csv", "result/id_test9870_mc.csv")
# column4_to_row("result/id_test9870_mc.csv", "data/XQ/candidate_entity_test_bert_9870_mc.txt", "result/xq_result_9870_mc")

