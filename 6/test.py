from vending_machine import VendingMachine

inventory = {
    "coke": 180,
    "water": 100,
    "tea": 120,
    "coffee": 80
}

def test_buy_item():
    for (item, price) in inventory.items():
        vm = VendingMachine(inventory)
        vm.insert_money(200)
        success = vm.buy(item)

        assert success
        assert vm.get_balance() == 200-price

        refund = vm.refund()
        assert refund == 200-price
        assert vm.get_balance() == 0

def test_buy_invalid_item():
    vm = VendingMachine({
        "coke": 180
    })
    vm.insert_money(1000)
    success = vm.buy("coffee")

    assert not success
    assert vm.get_balance() == 1000

def test_buy_insufficient_funds():
    vm = VendingMachine({
        "coke": 180
    })
    vm.insert_money(50)
    success = vm.buy("coke")

    assert not success
    assert vm.get_balance() == 50

def test_insert_negative_money():
    negative_money =  [-10, -50, -1000]
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
    test_buy_item()
    test_buy_invalid_item()
    test_buy_insufficient_funds()
    test_insert_negative_money()
    test_insert_invalid_money()