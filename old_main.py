import math
import argparse
from rulemodel import *
from SGMModel import *
import datetime
import networkx as nx
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument(
    "rules",
    type=str,
    help="読み込むルールファイルのパス. ClassBenchルール変換プログラムの6番を使用し,assign_evaluation_to_rulelist.pyで評価型を付与すること.")
parser.add_argument(
    "--packets",
    type=str,
    default=None,
    help="読み込むパケットファイルのパス.ClassBenchルール変換プログラムの6番を使用すること.無指定の場合は一様分布(全ての場合のパケット1つずつ).")
parser.add_argument(
    "--print_rulelist_detail",
    type=bool,
    default=False,
    help="ルールリストを出力するかどうか.")



if __name__ == "__main__":

    args = parser.parse_args()

    #ルールリストを形成
    rule_list = RuleList()
    
    with open(args.rules,mode="r") as rulelist_file:
        while rulelist_file:
            rule = rulelist_file.readline().split()
            #print(rule)
            if not rule:
                break
            rule_list.append(Rule(rule[0],rule[1]))

    #パケットリストを形成
    packet_list = []
    if args.packets != None:
        with open(args.packets,mode="r") as packetlist_file:
            while packetlist_file:
                packet = "".join(packetlist_file.readline().split())
                #print(packet)
                if not packet:
                    break
                packet_list.append(packet)
    else:
        max_num = 2**len(rule_list[0].bit_string)
        specifier = "0"+str(len(rule_list[0].bit_string))+"b"
        for i in range(max_num):
            packet_list.append(format(i,specifier))
            
    #リストをprintする場合はする
    if args.print_rulelist_detail:
        print(rule_list)

    #フィルタリング
    
    print("Start packet filtering.")
    res1 = rule_list.filter(packet_list,True,True)
    print("遅延合計値 = [%d]\n\nAll Packet is successfully filtered." % res1[0])
    print(res1[1])
    
    rule_list.compute_weight(packet_list)
    """
    for i in rule_list:
        print("%d,"%(i._weight),end="")
    print("")
    """
    # グラフ構築のテスト

    graph = SGM(rule_list)
    
    graph.plot_graph()
 
    rule_list2 = graph.sub_graph_mergine()
    print("Start packet filtering.")
    res2 = rule_list2.filter(packet_list,True,True)
    print("遅延合計値 = [%d]\n\nAll Packet is successfully filtered." % res2[0])
    print(res2[1])

    
    for i in range(len(res1[1])):
        if res1[1][i] != res2[1][i]:
            print("ERROR %d"%i)
            
    with open("Dump/DumpRule","w",encoding="utf-8",newline="\n") as write_file:
        for i in range(len(rule_list2)):
            if rule_list2[i].evaluate == "Accept":
                write_file.write("Accept\t"+rule_list2[i].bit_string+"\n")
            elif rule_list2[i].evaluate == "Deny":
                write_file.write("Deny\t"+rule_list2[i].bit_string+"\n")
