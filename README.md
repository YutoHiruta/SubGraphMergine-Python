# 概要
PythonでSGMを書いてみた。グラフのプロット機能つき。
※Python3.8？以上でのみ動作可能



# 仕様
## ライブラリ等とバージョン
### 基礎
- Python 3.8.6
- pip 19.3.1
### ライブラリ
- numpy 1.21.2
- matplotlib 3.4.3
- networkx 2.6.3

## 動作方法
`oldmain.py`を実行する。第1引数にルールリストを、`--packets`に、報酬計算に使うパケットリストを指定する。また、`--print_rulelist_detail=true`と書くと、ルールリストの詳細と従属関係を列挙する。
`--packets`を/指定しない場合、パケットリストは一様分布と仮定し、全てのパケットを一つずつ持つリストを作り、報酬計算に用いる。ゆえにリストの長さが2^xになるので、classbenchで生成したルールに対してはbit長が大きすぎて無指定は不可能。

SGMで並べ替えた後に、従属グラフをプロットして、並べ替え後のルールリストを出力する。
### コマンド例
	python3.8 old_main.py RuleList/assigned_Rule_acl5_500 --packets=PacketList/Packet_acl5_500 --print_rulelist_detail=true