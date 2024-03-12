# ======================================================================
# Checking Regular Expression Answers in Python (pyCREA)
#
# 計算理論の演習の採点において、
# 受講生の解答の正規表現が正答のものと等価なのかの判定を指定した長さ以下で行う
#
# このプログラムの動作は、具体的には、
# 1. 指定したアルファベット(alphabet)から指定した長さ(length)以下の系列を生成する
# 2. 生成した系列を"正答の正規表現"で「受理できる or 受理できない」に分類する
# 3. "受講生の解答の正規表現"が"正答の正規表現"の「受理できる or 受理できない」
#    と同じ分類であるかどうかを全探索することで「正しい可能性が高い or 誤答」を判定
# となっている
#
# (全探索するだけなので長さの値を大きくすると時間が掛かる...)
#
# Created on 2023/10/20, author: L3onSW
# ======================================================================
import re  # 正規表現(regular expression)のためのパッケージ
import itertools


def convert_to_python_notation(correct, ans):
    """convert_to_python_notation
    数学的な記法の正規表現をPythonの記法に書き換える

    Args:
        correct (str): 正答の正規表現の文字列
        ans (str): 受講生の解答の正規表現の文字列

    Returns:
        correct (str): 正答の正規表現の文字列
        ans (str): 受講生の解答の正規表現の文字列
    """
    tmp_correct = correct.replace("ε", "")
    tmp_ans = ans.replace("ε", "")
    correct = tmp_correct.replace("+", "|")
    ans = tmp_ans.replace("+", "|")
    return correct, ans


def get_string_list(alphabet, length, debug=False):
    """get_string_list
    指定したアルファベットから指定した長さ以下の系列すべてを生成する
      (例えば,アルファベット(alphabet)が["a", "b"]で長さ(length)が2なら,
       ε,a,b,aa,ab,ba,bbが生成される)

    なお,ここで生成した系列に対して,
    正答の正規表現で受理できるものが受講生の解答の正規表現でも正しく受理できるか,
    正答の正規表現で受理できないものが受講生の解答の正規表現でも正しく受理できないか
    を調べることで,正規表現が正しい可能性が高いor誤答を判断する

    Args:
        alphabet (list[str]): 正規表現を構成するアルファベットのリスト
        length (int):
          受講生の解答の正規表現が正答のものと等価なのかの判定を行う長さの最大値
          (この値以下の長さの系列に対して全探索で判定を行う)
        debug (bool, optional):
          正しくアルファベットが生成できているか表示.
          Trueだと表示、Falseだと非表示. デフォルトはFalse.

    Returns:
        string_list (str): 指定したアルファベットから生成した指定した長さ以下の系列のリスト
    """
    # 指定したアルファベットから指定した長さ以下の系列すべてを生成
    string_list = list()
    # εを先頭に格納
    string_list.append("")
    for i in range(1, length+1):
        # 指定したアルファベットから指定した長さ以下の系列すべてを生成
        # ただし改行などが入るので除去する
        for one_word in itertools.product(alphabet, repeat=i):
            string = ""  # 空の文字列で初期化する
            for j in range(len(one_word)):
                # 改行を除去する
                string += one_word[j].replace("¥n", "")
            # 指定したアルファベットの指定した長さ以下の系列を1つずつ格納していく
            string_list.append(string)
    # 指定したアルファベットから指定した長さ以下の系列すべてが正しく生成できているか確認する
    if debug is True:
        for i in range(len(string_list)):
            print(i+1, string_list[i])
    return string_list


def check_string_list(correct, string_list, debug=False):
    """check_string_list
    指定した長さ以下の系列すべてを正答の正規表現で受理できるor受理できないで分類する
      受理できる系列すべて:   acceptedに格納する
      受理できない系列すべて: rejectedに格納する

    Args:
        correct (str): 正答の正規表現
        string_list (list[str]):
          指定したアルファベットから生成した指定した長さ以下の系列のリスト
        debug (bool, optional):
          受理できるorできないの分類が正しいか表示.
          Trueだと表示、Falseだと非表示. デフォルトはFalse.

    Returns:
        accepted (list[str]): 正答の正規表現で受理できる系列のリスト
        rejected (list[str]): 正答の正規表現で受理できない系列のリスト
    """
    accepted = list()
    rejected = list()
    regular_expression = re.compile(correct)
    for i in range(len(string_list)):
        string = string_list[i]
        result = regular_expression.fullmatch(string)
        if result is not None:
            # 入力文字列全体が正規表現を満たした場合
            accepted.append(string)
        elif result is None:
            # 入力文字列全体が正規表現を満たさなかった場合
            rejected.append(string)
    # 正規表現で受理できる(accepted)or受理できない(rejected)の分類が正しいか確認する
    if debug is True:
        for i in range(len(accepted)):
            print("受理できる系列", accepted[i])
        print()
        for i in range(len(rejected)):
            print("受理できない系列", rejected[i])
    return accepted, rejected


def check_accepted(ans, accepted):
    """check_accepted
    受講生の解答の正規表現で受理されるべきものが受理されなかったら,
    反例として後に表示するためにリストに格納
      指定した長さ以下の本来受理できるべき系列すべてを,
      受講生の解答の正規表現でも正しく受理できるか調べる
      もし,受理できるはずなのに受理されない系列を見つけたら
      accidentally_rejectedに格納する

    Args:
        ans (str): 受講生の解答の正規表現
        accepted (list[str]): 受理されるべき正規表現のリスト

    Returns:
        accidentally_rejected (list[str]):
          受理されるべきなのに受理されない正規表現のリスト
    """
    accidentally_rejected = list()
    regular_expression = re.compile(ans)
    for i in range(len(accepted)):
        string = accepted[i]
        result = regular_expression.fullmatch(string)
        if result is None:
            accidentally_rejected.append(string)
    return accidentally_rejected


def check_rejected(ans, rejected):
    """check_rejected
    受講生の解答の正規表現で受理されるはずのないものが受理されてしまったら
    反例として後に表示するためにリストに格納
      指定した長さ以下の本来受理できないはずの系列すべてを,
      受講生の解答の正規表現でも正しく受理できないか調べる
      もし,受理できないはずなのに受理できてしまう系列を見つけたら
      accidentally_acceptedに格納する

    Args:
        ans (str): 受講生の解答の正規表現
        rejected (list[str]): 受理されてはいけない正規表現のリスト

    Returns:
        accidentally_accepted (list[str]):
          受理されないはずなのに受理されてしまう正規表現のリスト
    """
    accidentally_accepted = list()
    regular_expression = re.compile(ans)
    for i in range(len(rejected)):
        string = rejected[i]
        result = regular_expression.fullmatch(string)
        if result is not None:
            accidentally_accepted.append(string)
    return accidentally_accepted


def print_result(alphabet, length,
                 accidentally_rejected, accidentally_accepted, ans,
                 short=True, newline=True):
    """print_result
    受講生の解答の正規表現に対して判定の結果を表示する
    (あくまで指定した長さ以下での結果であることに注意する)

    指定した長さ以下の系列に対して,受講生の解答の正規表現が,
    受理できるはずなのに受理できない or
      受理できないはずなのに受理できてしまう系列が見つからなかった: 正しい可能性が高い
    受理できるはずなのに受理できない or
      受理できないはずなのに受理できてしまう系列が見つからなかった: 誤答
    なお,誤答の場合には反例を表示する

    Args:
        alphabet (list[str]): 正規表現を構成するアルファベットのリスト
        length (int):
          受講生の解答の正規表現が正答のものと等価なのかの判定を行う長さの最大値
          (この値以下の長さの系列に対して全探索で判定を行う)
        accidentally_rejected (list[str]):
          受理されるべきなのに受理されない正規表現のリスト
        accidentally_accepted (list[str]):
          受理されないはずなのに受理されてしまう正規表現のリスト
        ans (str): 受講生の解答の正規表現
        short (bool, optional):
          表示する見つけた反例の個数
          Trueだと1個、Falseだと全て(1個以上の複数個). デフォルトはTrue.
        newline (bool, optional):
          最後に改行を表示するかどうか.
          Trueだと表示、Falseだと非表示. デフォルトTrue.
    """
    if len(accidentally_rejected) == 0 and len(accidentally_accepted) == 0:
        # 受講受講生の正規表現が正しい可能性が高い場合
        # （指定した長さ以下の系列では正しく受理できるor受理できないが動作した場合）
        print(ans + " は正しい可能性が高いです")
        print("  アルファベットΣ={", end="")
        for i in range(len(alphabet)-1):
            print(alphabet[i], end=",")
        print(alphabet[len(alphabet)-1], end="")
        print("}から構成される長さ" + str(length) + "以下の全ての系列を調べました")
    else:
        # 受講受講生の正規表現が誤答の場合
        print(ans + " は誤答です")
        if short is True:
            # 反例を1つだけ表示する
            if len(accidentally_rejected) >= 1:
                if accidentally_rejected[0] != "":
                    print("  受理できるはずの系列が受理されませんでした:", end=" ")
                    print(accidentally_rejected[0])
                else:
                    print("  受理できるはずの系列が受理されませんでした:", end=" ")
                    print("ε")
            if len(accidentally_accepted) >= 1:
                if accidentally_accepted[0] != "":
                    print("  受理できないはずの系列が受理されてしまいました:", end=" ")
                    print(accidentally_accepted[0])
                else:
                    print("  受理できないはずの系列が受理されてしまいました:", end=" ")
                    print("ε")
        else:
            # 反例を見つけただけ(1つ以上)表示する
            for i in range(len(accidentally_rejected)):
                if accidentally_rejected[i] != "":
                    print("  受理できるはずの系列が受理されませんでした:", end=" ")
                    print(accidentally_rejected[i])
                else:
                    print("  受理できるはずの系列が受理されませんでした:", end=" ")
                    print("ε")
            for i in range(len(accidentally_accepted)):
                if accidentally_accepted[i] != "":
                    print("  受理できないはずの系列が受理されてしまいました:", end=" ")
                    print(accidentally_accepted[i])
                else:
                    print("  受理できないはずの系列が受理されてしまいました:", end=" ")
                    print("ε")
    # 最後に改行を表示するかどうか
    # (続けて複数個の解答の判定をするならTrue,1つの解答だけならElseが良さげ)
    if newline is True:
        print()


def check(correct, ans, alphabet, length=10):
    """check
    1個の受講生の正規表現に対して
    正答のものと等価なのかの判定を行うことで
    正しい可能性が高い or 誤答 の判定を行う

    Args:
        correct (str): 正答の正規表現
        ans (str): 受講生の解答の正規表現
        alphabet (list[str]): 正規表現を構成するアルファベットのリスト
        length (int, optional):
          受講生の解答の正規表現が正答のものと等価なのかの判定を行う長さの最大値
          (この値以下の長さの系列に対して全探索で判定を行う)
          デフォルトは10(問題にもよるがこれくらいがちょうど良さそう).
    """
    # 学生のした解答の正規表現を最後に表示で使うようにとっておく
    ans_print = ans

    # 数学的な記法(計算理論及び演習での記法)の正規表現をPythonの記法に書き換える
    correct, ans = convert_to_python_notation(correct, ans)

    # 指定したアルファベットから指定した長さ以下の系列すべてを生成し,string_listに格納する
    string_list = get_string_list(alphabet, length)

    # 指定した長さ以下の系列すべてを正答の正規表現で受理できるor受理できないで分類する
    # 正答の正規表現で受理できる系列はaccepted,受理できない系列はrejectedに格納する
    accepted, rejected = check_string_list(correct, string_list)

    # 受講生の解答の正規表現で受理されるべきものが受理されなかったら
    # 反例として後に表示するためにaccidentally_rejectedに格納
    accidentally_rejected = check_accepted(ans, accepted)

    # 受講生の解答の正規表現で受理されるはずのないものが受理されてしまったら
    # 反例として後に表示するためにaccidentally_acceptedに格納
    accidentally_accepted = check_rejected(ans, rejected)

    # 受講生の解答の正規表現に対して判定の結果を表示する
    # (あくまで指定した長さ(length)以下での結果であることに注意する)
    print_result(alphabet, length,
                 accidentally_rejected, accidentally_accepted, ans_print)


def check_multiple(input_filename, alphabet, length):
    """check_multiple
    複数個の受講生の正規表現に対して
    正答のものと等価なのかの判定を行うことで
    正しい可能性が高い or 誤答 の判定を行う

    Args:
        input_filename (str):
          1行目に正答の正規表現,2行目から下に受講生の解答の正規表現を格納したファイル
          のファイル名
        alphabet (list[str]): 正規表現を構成するアルファベットのリスト
        length (int, optional):
          受講生の解答の正規表現が正答のものと等価なのかの判定を行う長さの最大値
          (この値以下の長さの系列に対して全探索で判定を行う)
          デフォルトは10(問題にもよるがこれくらいがちょうど良さそう).
    """
    f = open(input_filename, "r")
    check_list = f.readlines()

    # 入力ファイル1行目を正答の正規表現とする
    correct = check_list[0].replace("¥n", "")

    # 入力ファイル2行目から順番に正答の正規表現と等価か調べる
    for i in range(1, len(check_list)):
        ans = check_list[i].replace("¥n", "")
        check(correct, ans, alphabet, length=10)
