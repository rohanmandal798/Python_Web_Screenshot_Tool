import unittest
from unittest.mock import patch, MagicMock
import os
from selenium.common.exceptions import WebDriverException
from Screenshot_Tool import ensure_full_url, capture_screenshot

class TestScreenshotTool(unittest.TestCase):

    def test_ensure_full_url(self):
        # Test with valid URLs
        self.assertEqual(ensure_full_url("example.com"), "https://example.com")
        self.assertEqual(ensure_full_url("http://example.com"), "http://example.com")
        self.assertEqual(ensure_full_url("https://example.com"), "https://example.com")

        # Test with invalid URLs
        self.assertEqual(ensure_full_url(""), "https://")
        self.assertEqual(ensure_full_url("ftp://example.com"), "https://ftp://example.com")

    @patch('screenshot_tool.webdriver.Firefox')
    @patch('screenshot_tool.Service')
    def test_capture_screenshot_success(self, mock_service, mock_firefox):
        # Mock the WebDriver and its methods
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver
        mock_driver.current_url = "https://example.com"
        
        # Mock the save_screenshot method
        mock_driver.save_screenshot = MagicMock(return_value=None)
        
        output_folder = "test_output"
        os.makedirs(output_folder, exist_ok=True)

        # Call the function
        result = capture_screenshot("https://example.com", output_folder)

        # Check that the screenshot was saved
        mock_driver.save_screenshot.assert_called_once_with(os.path.join(output_folder, "example.com.png"))
        self.assertTrue(result)

        # Clean up
        mock_driver.quit()

    @patch('screenshot_tool.webdriver.Firefox')
    @patch('screenshot_tool.Service')
    def test_capture_screenshot_failure(self, mock_service, mock_firefox):
        # Mock the WebDriver to raise an exception when get is called
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver
        
        # Set the side effect for the get method to raise an exception
        mock_driver.get.side_effect = WebDriverException("DNS resolution failed")

        output_folder = "test_output"
        os.makedirs(output_folder, exist_ok=True)

        # Call the function
        result = capture_screenshot("https://example.com", output_folder)

        # Check that the result is False due to failure
        self.assertFalse(result)

        # Clean up
        mock_driver.quit()

if __name__ == '__main__':
    unittest.main()
