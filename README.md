[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# Checking Regular Expression Answers in Python (pyCREA)
受講生の解答の正規表現に対して「正答の可能性が高い or 誤答である」を判定します。
- [![python-shield]][python-url]で書かれています。
- [丸岡 章. 計算理論とオートマトン言語理論 [第2版]. サイエンス社, 2021年.][theory-of-computation-textbook-url]の記法を文字列として書けば使えます。
- 度々出てくるpyCREAとは、Checking Regular Expression Answers in Pythonの略です。

## 🚨 注意点
- あくまで変数lengthで指定した長さ以下での判定になります。
- 変数lengthの値を大きくすると、全探索をしているために時間がかかります。
- 正規表現を指定する箇所に無駄なスペースがあると正しく判定できなくなります。
  - ❌：`ans = "(b(a+b))*a((a+b)a) *"`
    - 上記のように無駄なスペースがあると正しく判定できません。
    - 上記だと最後のアスタリスクの前に半角スペースが無駄に存在しています。
  - ⭕️：`ans = "(b(a+b))*a((a+b)a)*"`
    - 上記のように無駄なスペースがないものにしてください。

## 🧑‍💻 使用方法
### 1個ずつ判定する場合 (例: [example1.py][example1.py-url])
1. pyCREA.pyを同じディレクトリに置いて、以下の[example1.py][example1.py-url]を作成します。
2. `python example1.py`で実行します。
```python
import pyCREA

# 解答を判定したい問題についての準備
correct = "(0+1)*11"  # 正答の正規表現 (0+1)*11
alphabet = ["0", "1"]  # 正規表現を構成するアルファベット Σ={0,1}
length = 10  # この長さ以下の系列を判定する

# 受講生の解答の正規表現 (0+1+00+11+01+10)*111* に対する判定
ans = "(0+1+00+11+01+10)*111*"  # 受講生の解答の正規表現
pyCREA.check(correct, ans, alphabet, length)  # 判定

# 受講生の解答の正規表現 0(0+1)*11 に対する判定
ans = "0(0+1)*11"  # 受講生の解答の正規表現
pyCREA.check(correct, ans, alphabet, length)  # 判定

# 受講生の解答の正規表現 ε に対する判定
ans = "ε"  # 受講生の解答の正規表現
pyCREA.check(correct, ans, alphabet, length)  # 判定

# 受講生の解答の正規表現 (ε+0+1)*
ans = "(ε+0+1)*"  # 受講生の解答の正規表現
pyCREA.check(correct, ans, alphabet, length)  # 判定
```

### 複数個同時に判定する場合 (例: [example2.py][example2.py-url] + [example2_input.txt][example2_input.txt-url])
1. pyCREA.pyを同じディレクトリに置いて、以下の[example2.py][example2.py-url]を作成します。
2. 1行目に正答の正規表現、2行目から下に学生の解答の正規表現を書いた[example2_input.txt][example2_input.txt-url]を作成します。
3. `python example2.py`で実行します。
```python
import pyCREA

# 1行目に正答,2行目から下に受講生の解答を格納したファイルに対して判定を行う
input_file = "example_input.txt"  # 1行目に正答,2行目から下に受講生の解答を格納したファイル
alphabet = ["0", "1"]  # 正規表現を構成するアルファベット Σ={0,1}
length = 10  # この長さ以下の系列を判定する
pyCREA.check_multiple(input_file, alphabet, length)  # 判定
```

### 実行結果例
[example1.py][example1.py-url]を実行した結果は以下のようになります。([example2.py][example2.py-url]でも同様です。)
```console
L3on@MacBook:pyCREA$ python example1.py 
 (0+1+00+11+01+10)*111* は正しい可能性が高いです
   アルファベットΣ={0,1}から構成される長さ10以下の全ての系列を調べました

 0(0+1)*11 は誤答です
   受理できるはずの系列が受理されませんでした: 11

 ε は誤答です
   受理できるはずの系列が受理されませんでした: 11
   受理できないはずの系列が受理されてしまいました: ε

 (ε+0+1)* は誤答です
   受理できないはずの系列が受理されてしまいました: ε
```

### pyCREAの変数とその役割
| 変数 | 役割 |
| --- | --- |
| correct | 正答の正規表現 |
| alphabet | 正規表現を構成するアルファベット |
| length | 全探索する系列の最大の長さ(この長さ以下の系列全てを全探索します) |
| ans | 受講生の解答の正規表現 |


## 💻 環境
- Python 3.8.3
  - pyCREAを作成した環境は上記ですが、特殊な記法やパッケージは使用していないため、上記以外のバージョンであっても一般的なPython環境があれば動くように思います。

## 🛠️ 開発方法のお願い
pyCREAを作成した動機は、TA(Teaching Assistant)の業務の1つである答案の採点時に、
等価な正規表現が大量にあることで正答と誤答の判別が非常に大変だったことです。

そのため、かなり限定的な使い方を目的としたプログラムになっています。  
よって、今後の発展はあまり無いように思います。  
(今後については、書き方がダサい点などに対処することはあるかもしれません。)

もし、開発にご協力いただけるようでしたら、以下の方法に従っていただけますと幸いです。

- 本リポジトリに対する開発：個別のブランチを切って作業をお願いします。
- 実装した新規機能の反映：mainブランチに対して[Pull Request(PR)][pull-requests-url]してください。
- バグ報告，新規機能の要望・提案など：本リポジトリの[Issues][issues-url]からお願いします。

## 📚 参考文献
1. [丸岡 章. "計算理論とオートマトン言語理論 [第2版]". サイエンス社, 2021年.][theory-of-computation-textbook-url]
2. ["Pythonの正規表現モジュールreの使い方（match, search, subなど）". note.nkmk.me. (参照：2024-03-12).][python-re-note-nkmk-me-url]
3. ["itertools --- 効率的なループ実行のためのイテレータ生成関数". Python 3.12.2 ドキュメント. (参照：2024-03-12).][python-itertools.product-url]

<!--
========================================================================
本README.mdで使用しているリンク
========================================================================
-->
<!-- 
------------------------------------------------------------------------
GitHub関連
------------------------------------------------------------------------
-->
<!-- Contributors -->
[contributors-shield]: https://img.shields.io/github/contributors/L3onSW/pyCREA.svg?style=for-the-badge
[contributors-url]: https://github.com/L3onSW/pyCREA/graphs/contributors
<!-- Forks -->
[forks-shield]: https://img.shields.io/github/forks/L3onSW/pyCREA.svg?style=for-the-badge
[forks-url]: https://github.com/L3onSW/pyCREA/network/members
<!-- Stars -->
[stars-shield]: https://img.shields.io/github/stars/L3onSW/pyCREA.svg?style=for-the-badge
[stars-url]: https://github.com/L3onSW/pyCREA/stargazers
<!-- Isuues -->
[issues-shield]: https://img.shields.io/github/issues/L3onSW/pyCREA.svg?style=for-the-badge
[issues-url]: https://github.com/L3onSW/pyCREA/issues
<!-- License -->
[license-shield]: https://img.shields.io/github/license/L3onSW/pyCREA.svg?style=for-the-badge
[license-url]: https://github.com/L3onSW/pyCREA/blob/master/LICENSE
<!-- Pull Requests -->
[pull-requests-url]: https://github.com/L3onSW/pyCREA/pulls

<!-- example1.py -->
[example1.py-url]: https://github.com/L3onSW/pyCREA/blob/master/example1.py
<!-- example2.py -->
[example2.py-url]: https://github.com/L3onSW/pyCREA/blob/master/example2.py
<!-- example2_input.txt -->
[example2_input.txt-url]: https://github.com/L3onSW/pyCREA/blob/master/example2_input.txt

<!-- 
------------------------------------------------------------------------
その他Webページ(参考文献など)
------------------------------------------------------------------------
-->
<!-- Python -->
[python-shield]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[python-url]: https://www.python.org
<!-- 丸岡 章. 計算理論とオートマトン言語理論 [第2版]　-->
[theory-of-computation-textbook-url]: https://www.saiensu.co.jp/search/?isbn=978-4-7819-1521-0&y=2021
<!-- Pythonの正規表現モジュールreの使い方（match, search, subなど）-->
[python-re-note-nkmk-me-url]: https://note.nkmk.me/python-re-match-search-findall-etc/
<!-- itertools.product -->
[python-itertools.product-url]: https://docs.python.org/ja/3/library/itertools.html#itertools.product
