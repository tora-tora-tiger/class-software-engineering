## 自動販売機クラス
### 仕様
- 商品と価格は、Pythonの辞書を使い、`商品名: 価格`で定義をする
メソッド
- お金を入れる
	- 引数: 金額
	- 戻り値: 入った金額
- 現在入っているお金を見る
	- 引数: なし
	- 戻り値: 入った金額
- 商品を買う
	-  引数: `"coke" | "water" | "tea" | "coffee"` など商品名
	- 戻り値: `True | False` 成功したか
- お釣りを出す
	- 金額 なければ0

---
### テストシナリオ
- 商品を買える・買ったあとにお金が減る・お釣りが返ってくる
- 買うときにお金が足りない場合はfalse
- 買うときに商品が存在しない注文はfalse
- 負の金額は入れられない
- 投入できる金額は正整数

### 開発のサイクル
テストケース: 商品を買える。買ったあとにお金が減る・お釣りが返ってくる
```python
def test_buy_item():
	inventory = {
	    "coke": 180,
	    "water": 100,
	    "tea": 120,
	    "coffee": 80
	}
    for (item, price) in inventory.items():
        vm = VendingMachine(inventory)
        vm.insert_money(200)
        success = vm.buy(item)

        assert success
        assert vm.get_balance() == 200-price
```
作成したコード
```python
class VendingMachine:
    def __init__(self, inventory):
        self.balance = 0
        self.inventory = inventory

    def insert_money(self, amount):
	    price = self.inventory[item]
        self.balance += amount
        return self.balance
    
    def get_balance(self):
        return self.balance

    def buy(self, item):
        self.balance -= price
        return True
    
    def refund(self):
        refunded_amount = self.balance
        self.balance = 0
        return refunded_amount
```

テストケース: 買う時に商品が存在しない場合はfalse
```python
def test_buy_invalid_item():
    vm = VendingMachine({
        "coke": 180
    })
    vm.insert_money(1000)
    success = vm.buy("coffee")

    assert not success
    assert vm.get_balance() == 1000
```
作成したコード(差分)
```diff
    def buy(self, item):
+       if item not in self.inventory:
+           return False
```

テストケース: 買う時にお金が足りない場合はfalse
```python
def test_buy_insufficient_funds():
    vm = VendingMachine({
        "coke": 180
    })
    vm.insert_money(50)
    success = vm.buy("coke")

    assert not success
    assert vm.get_balance() == 50
```
作成したコード(差分)
```diff
def buy(self, item):
    if item not in self.inventory:
        return False
    price = self.inventory[item]
+   if self.balance < price:
+       return False
```

テストケース: 負の金額は入れられない
```python
def test_insert_negative_money():
    negative_money =  [-10, -50, -1000]
    vm = VendingMachine(inventory)
    for amount in negative_money:
        balance = vm.insert_money(amount)
        assert balance == 0
        assert vm.get_balance() == 0
```
作成したコード(差分)
```diff
	def insert_money(self, amount):
+        if amount < 0:
+            return self.balance
```

テストケース: 投入できる金額は整数
```python
def test_insert_invalid_money():
    invaild_money = [0.5, "100", None, [], {}]
    vm = VendingMachine(inventory)
    for amount in invaild_money:
        balance = vm.insert_money(amount)
        assert balance == 0
        assert vm.get_balance() == 0
```
作成したコード(差分)
```diff
	def insert_money(self, amount):
+        if not isinstance(amount, int):
+            return self.balance
```