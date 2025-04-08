import pytest

def get_plugin_version():
    """Get the plugin version."""
    return "1.0.0"

def test_get_plugin_version():
    """Test the get_plugin_version function."""
    version = get_plugin_version()
    assert version == '1.0.0'

if __name__ == '__main__':
    pytest.main() 