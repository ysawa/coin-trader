# 仮想通貨ボット

暗号通貨を売買するために使うボットです。趣味程度です。
BitFlyer に対応しています。 Zaif も書いてみましたが、いろんな意味で非推奨です。

## インストール

Python 3系をインストールしてください。その後、必要なパッケージをインストール。

```bash
pip install -r requirements.txt
```

## 設定

`setttings.py` を編集します。

```bash
cp settings.py.sample settings.py
```

## 利用方法

各サンプルスクリプトも参考にごらんください。

```python
from bitflyer.api import BitflyerApi

bitflyer_api = BitflyerApi()
last_price = bitflyer_api.request_last_price()
print('BitFlyer LAST PRICE: {} JPY/BTC'.format(last_price))
```

### 売買

`0.001` BTC を成行注文(買い)する場合。
第2引数を `False` にすると、売り注文になる。
指値注文する場合は、第3引数に価格日本円を指定する。
`child_order_acceptance_id` は、キャンセル時などに使える。

```python
from bitflyer.api import BitflyerApi

bitflyer_api = BitflyerApi()
child_order_acceptance_id = bitflyer_api.request_trade('0.001', True)
print('BitFlyer child_order_acceptance_id: ', child_order_acceptance_id)
```

## 免責

開発者は、当プログラムのご利用において生じたいかなる損害・障害・損失・不具合（ご利用中のコンピュータ、ソフトウェアの環境等に生じた障害等）に対して責任・賠償等、一切の義務を負いません。