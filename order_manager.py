import json
from typing import List, Dict, Any

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_orders(file_name: str) -> List[Dict[str, Any]]:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_orders(orders: List[Dict[str, Any]], file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)


def add_order(orders: List[Dict[str, Any]]) -> None:
    order_id = input("請輸入訂單編號：").upper()
    if any(order["order_id"] == order_id for order in orders):
        print(f"=> 錯誤：訂單編號 {order_id} 已存在！")
        return
    customer = input("請輸入顧客姓名：")
    items = []
    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：")
        if not name:
            break
        while True:
            try:
                price = int(input("請輸入價格："))
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")
        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        print("=> 至少需要一個訂單項目")
        return

    orders.append({"order_id": order_id, "customer": customer, "items": items})
    save_orders(orders, INPUT_FILE)
    print(f"=> 訂單 {order_id} 已新增！")


def display_orders(orders: List[Dict[str, Any]], title: str = "訂單列表") -> None:
    if not orders:
        print("目前沒有訂單。")
        return

    print(f"\n==================== {title} ====================")
    for i, order in enumerate(orders):
        if title != "出餐訂單":  # 只有在不是出餐訂單時才顯示
            print(f"訂單 #{i + 1}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print(f"{'商品名稱'}\t{'單價'}\t{'數量'}\t{'小計'}")  # 修改此行
        print("-" * 50)
        for item in order["items"]:
            name = item["name"]
            price = f"{item['price']:,}"
            quantity = str(item["quantity"])
            subtotal = f"{item['price'] * item['quantity']:,}"
            print(f"{name:<8}\t{price:<6}\t{quantity:<4}\t{subtotal:<6}")
        total = sum(item["price"]*item["quantity"] for item in order["items"])
        print("-" * 50)
        print(f"訂單總額: {total:,}")
        print("=" * 50)


def process_order(orders: List[Dict[str, Any]],
                  output_orders: List[Dict[str, Any]]) -> None:
    if not orders:
        print("目前沒有待處理訂單。")
        return

    print("待處理訂單：")
    for order in orders:
        print(f"{order['order_id']}: {order['customer']}")

    order_id = input("請輸入要出餐的訂單編號（Enter 取消）：").upper()
    if not order_id:
        return

    for i, order in enumerate(orders):
        if order["order_id"] == order_id:
            output_orders.append(orders.pop(i))
            save_orders(orders, INPUT_FILE)
            save_orders(output_orders, OUTPUT_FILE)
            print("=> 訂單 {order['order_id']} 已出餐完成\n出餐訂單詳細資料：")
            display_orders([output_orders[-1]], "出餐訂單")
            return

    print("找不到該訂單。")


def main():
    orders = load_orders(INPUT_FILE)
    output_orders = load_orders(OUTPUT_FILE)

    while True:
        print("\n***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")

        choice = input("請選擇操作項目(1~4)：")

        if choice == "1":
            add_order(orders)
        elif choice == "2":
            display_orders(orders, "訂單列表")
        elif choice == "3":
            process_order(orders, output_orders)
        elif choice == "4":
            print("感謝使用，再見！")
            break
        else:
            print("=> 請輸入有效的選項（1~4）")


if __name__ == "__main__":
    main()
