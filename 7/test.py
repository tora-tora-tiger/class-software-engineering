from vending_machine import VendingMachine
from hypothesis import given, strategies as st

inventory = {
    "coke": 180,
    "water": 100,
    "tea": 120,
    "coffee": 80
}

@given(
    st.dictionaries(
        st.text(min_size=1, alphabet=st.characters(codec="ascii")),  # 商品名
        st.integers(min_value=1, max_value=1000),  # 価格の範囲
        min_size=1,
        max_size=100
    ),
    st.integers(min_value=0, max_value=500)  # 追加金額
)
def test_buy_item_with_extra(test_inventory, extra_amount):
    """
    test_inventory: テスト用の商品辞書 {商品名: 価格}
    extra_amount: 商品価格に加える追加金額
    """

    for item, price in test_inventory.items():
        vm = VendingMachine(test_inventory)
        total_money = price + extra_amount

        # お金を投入
        vm.insert_money(total_money)
        success = vm.buy(item)

        # 購入成功の検証
        assert success, f"{item}({price}円) を {total_money} 円で購入しようとして失敗"

        # 残金が追加金額と一致するか検証
        assert vm.get_balance() == extra_amount, f"残金 {extra_amount}円が予想されるところ,  {vm.get_balance()}円"

        # 払い戻しの検証
        refund = vm.refund()
        assert refund == extra_amount, f"払い戻し額 {extra_amount}円が予想されるところ, {refund}円"
        assert vm.get_balance() == 0, "返金後0円でない"

def test_buy_invalid_item():
    vm = VendingMachine({
        "coke": 180
    })
    vm.insert_money(1000)
    success = vm.buy("coffee")

    # 購入失敗の検証
    assert not success, "存在しない商品を購入できてしまった"
    assert vm.get_balance() == 1000, "投入金額が変わってしまっている"

def test_buy_insufficient_funds():
    vm = VendingMachine({
        "coke": 180
    })
    vm.insert_money(50)
    success = vm.buy("coke")

    # 購入失敗の検証
    assert not success, "不足金額で商品を購入できてしまった"
    assert vm.get_balance() == 50, "購入してないのに投入金額が変わってしまっている"

def test_insert_negative_money():
    negative_money = [-10, -50, -1000]
    vm = VendingMachine(inventory)
    for amount in negative_money:
        balance = vm.insert_money(amount)
        assert balance == 0
        assert vm.get_balance() == 0

def test_insert_invalid_money():
    invalid_money = [0.5, 1+1j, "100", None, [], {}]
    vm = VendingMachine(inventory)
    for amount in invalid_money:
        balance = vm.insert_money(amount)
        assert balance == 0
        assert vm.get_balance() == 0

if __name__ == "__main__":
    test_buy_item_with_extra()
    test_buy_invalid_item()
    test_buy_insufficient_funds()
    test_insert_negative_money()
    test_insert_invalid_money()