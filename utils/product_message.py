def product_message(product: dict) -> str:
    message = (
        f"В акцию добавлен новый товар:\n\n"
        f"Название акции: {product['action_title']}\n"
        f"Название товара: {product['name']}\n"
        f"Старая цена: {product['price']} руб.\n"
        f"Цена по акции: {product['action_price']} руб.\n"
    )
    return message
