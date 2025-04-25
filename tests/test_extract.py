import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from utils.extract import fetch_content, extract_product_data, scrape_product_async


# --- Test Constants ---
SAMPLE_HTML = """
<html>
  <div class="collection-grid" id="collectionList">
    <div class="collection-card">
      <h3 class="product-title">Test Product</h3>
      <span class="price">$10.99</span>
      <p style="font-size: 14px; color: #777;">Rating: 4.5</p>
      <p style="font-size: 14px; color: #777;">3 Colors</p>
      <p style="font-size: 14px; color: #777;">Size: M</p>
      <p style="font-size: 14px; color: #777;">Gender: Men</p>
    </div>
  </div>
</html>
"""

# --- Fixtures ---
@pytest.fixture
def mock_product_card():
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    return soup.find("div", class_="collection-card")

# --- Tests ---
@pytest.mark.asyncio
async def test_fetch_content_success():
    # Create a mock session
    mock_session = AsyncMock()
    
    # Create a mock response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value=SAMPLE_HTML)
    
    # Set up the async context manager chain
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    # Create a proper semaphore mock
    mock_semaphore = AsyncMock()
    # Simulate semaphore __aenter__ and __aexit__
    mock_semaphore.__aenter__ = AsyncMock(return_value=None)
    mock_semaphore.__aexit__ = AsyncMock(return_value=None)
    
    # Call the function
    content = await fetch_content(
        session=mock_session,
        url="http://test.com",
        semaphore=mock_semaphore,
        retry=0
    )
    
    # Verify the result
    assert content == SAMPLE_HTML
    
    # Verify the mocks were called correctly
    mock_session.get.assert_called_once_with(
        "http://test.com",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
    )
    mock_response.text.assert_awaited_once()

def test_extract_product_data(mock_product_card):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    product = extract_product_data(mock_product_card, timestamp)
    
    assert product["Title"] == "Test Product"
    assert product["Price"] == "$10.99"
    assert product["Rating"] == "Rating: 4.5"
    assert product["Colors"] == "3 Colors"

@pytest.mark.asyncio
@patch("utils.extract.scrape_pages_batch", new_callable=AsyncMock)
async def test_scrape_product_async(mock_scrape_batch):
    mock_scrape_batch.return_value = [{"Title": "Test Product"}]
    
    products = await scrape_product_async("http://test.com/page{}", max_pages=1)
    assert len(products) == 1
    assert products[0]["Title"] == "Test Product"