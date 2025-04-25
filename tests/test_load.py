import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from unittest.mock import patch, AsyncMock
import pandas as pd
import os
from datetime import datetime
from utils.load import save_to_csv

# --- Fixtures ---
@pytest.fixture
def sample_dataframe():
    """Return a minimal valid DataFrame for testing."""
    return pd.DataFrame({
        "Title": ["Product 1", "Product 2"],
        "Price": [10000, 20000]
    })

@pytest.fixture
def empty_dataframe():
    """Return an empty DataFrame for testing."""
    return pd.DataFrame()

# --- Tests ---
@pytest.mark.asyncio
async def test_save_to_csv_success(sample_dataframe, tmp_path):
    with patch("utils.load.datetime") as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "20230101_123456"
        saved_path = await save_to_csv(sample_dataframe)
        
        assert saved_path.endswith("fashion_products_20230101_123456.csv")
        assert os.path.exists(saved_path)

@pytest.mark.asyncio
async def test_save_to_csv_custom_filename(sample_dataframe, tmp_path):
    """Test CSV save with custom filename."""
    custom_path = tmp_path / "custom_dir/custom_file.csv"
    saved_path = await save_to_csv(sample_dataframe, str(custom_path))
    
    assert saved_path == str(custom_path)
    assert os.path.exists(saved_path)
    assert pd.read_csv(saved_path).equals(sample_dataframe)

@pytest.mark.asyncio
async def test_save_to_csv_empty_data(empty_dataframe, capsys):
    """Test handling of empty DataFrame."""
    result = await save_to_csv(empty_dataframe)
    
    assert result is None
    captured = capsys.readouterr()
    assert "No data to save" in captured.out

@pytest.mark.asyncio
async def test_directory_creation(sample_dataframe, tmp_path):
    """Test automatic directory creation."""
    custom_path = tmp_path / "new_dir/subdir/output.csv"
    await save_to_csv(sample_dataframe, str(custom_path))
    
    assert os.path.exists(custom_path.parent)
    assert os.path.isfile(custom_path)

@pytest.mark.asyncio
@patch("asyncio.to_thread", new_callable=AsyncMock)
async def test_async_io_handling(mock_to_thread, sample_dataframe):
    """Verify async-to-thread delegation works."""
    mock_to_thread.return_value = "dummy_path.csv"
    await save_to_csv(sample_dataframe)
    
    mock_to_thread.assert_awaited_once()