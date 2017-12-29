# 仮想通貨ボット

暗号通貨を売買するために使うボットです。趣味程度です。

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

各サンプルスクリプトを参考にしてください。

# 0.001 BTC を 購入(True) する (成行)
# child_order_acceptance_id は、キャンセル時などに使える
# result = bitflyer_api.request_trade('0.001', True)

```python
from bitflyer.api import BitflyerApi

bitflyer_api = BitflyerApi()
last_price = bitflyer_api.request_last_price()
print('BitFlyer LAST PRICE: {} JPY/BTC'.format(last_price))
```

### 売買

`0.001` BTC を 成行注文( `True` ) する場合。指値注文する場合は、第三引数に価格日本円を指定する。
`child_order_acceptance_id` は、キャンセル時などに使える。

```python
from bitflyer.api import BitflyerApi

bitflyer_api = BitflyerApi()
result = bitflyer_api.request_trade('0.001', True)
print('BitFlyer child_order_acceptance_id: ', result)
```

## 免責