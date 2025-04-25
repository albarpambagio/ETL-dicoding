from datetime import datetime
from bs4 import BeautifulSoup
from utils.extract import extract_product_data

def test_extract_product_data():
    html = '''
    <div class="collection-card">
        <h3 class="product-title">Cool T-Shirt</h3>
        <span class="price">$25.50</span>
        <p style="font-size: 14px; color: #777;">Rating: 4.5/5</p>
        <p style="font-size: 14px; color: #777;">Colors: 3 Colors</p>
        <p style="font-size: 14px; color: #777;">Size: M</p>
        <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div', class_='collection-card')
    product = extract_product_data(card)

    assert product['Title'] == 'Cool T-Shirt'
    assert product['Price'] == '$25.50'
    assert product['Rating'] == 'Rating: 4.5/5'
    assert product['Colors'] == 'Colors: 3 Colors'
    assert product['Size'] == 'Size: M'
    assert product['Gender'] == 'Gender: Unisex'
    try:
        datetime.strptime(product['Timestamp'], '%Y-%m-%d %H:%M:%S')
        assert True  # Passes if parsing succeeds
    except ValueError:
        assert False, "Invalid timestamp format"
