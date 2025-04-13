# Sample Affiliate Links (Replace with real API keys)
SHOP_APIS = {
    "hm": "https://apix.example.com/hm/products",
    "myntra": "https://api.myntra.com/v1/search",
    "ajio": "https://ajioapi.com/items"
}

def get_shopping_links(items, category="all"):
    """Get shopping links for detected items"""
    # Sample Implementation
    return [
        {
            "name": "Striped Cotton Shirt",
            "store": "H&M",
            "price": 29.99,
            "url": "https://hm.com/shirt123",
            "image": "assets/hm_shirt.jpg"
        },
        {
            "name": "Slim Fit Jeans",
            "store": "Myntra",
            "price": 49.99,
            "url": "https://myntra.com/jeans456",
            "image": "assets/myntra_jeans.jpg"
        }
    ]