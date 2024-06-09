def product_message(product: dict) -> str:
    message = (
        f"**В акцию добавлен новый товар:**\n"
        f"Название товара: {product['name']}\n"
        f"Старая цена: {product['price']} руб.\n"
        f"Цена по акции: {product['action_price']} руб.\n"
    )
    return message