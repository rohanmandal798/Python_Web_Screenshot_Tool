import os
import sys
import time
import threading
import validators
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException


# Ensure URLs have "https://"
def ensure_full_url(url):
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url


# Capture screenshot (runs in multiple threads)
def capture_screenshot(url, output_folder):
    """ Captures a screenshot using a separate Firefox WebDriver instance for each thread """
    options = Options()
    options.add_argument("--headless")
    options.log.level = "fatal"  # Suppress logs
    service = Service(r"C:\geckodriver-v0.35.0-win64\geckodriver.exe")  # Update with your path

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(30)
    driver.set_window_size(1920, 1080)

    attempt = 0
    while attempt < 3:
        try:
            driver.get(url)
            time.sleep(5)  # Wait for page to load

            if "about:neterror" in driver.current_url:
                raise WebDriverException("DNS resolution failed")

            domain = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
            file_name = os.path.join(output_folder, f"{domain}.png")

            driver.save_screenshot(file_name)
            driver.quit()
            return True
        except WebDriverException:
            attempt += 1
            time.sleep(5)

    # Log failed URLs
    with threading.Lock():
        with open(os.path.join(output_folder, "failed_urls.txt"), "a") as f:
            f.write(url + "\n")

    driver.quit()
    return False


# Main function to handle input file or single URL
def capture_screenshots(input_value, output_folder):
    """ Handles multithreading for fast screenshot capturing """
    urls = []

    if os.path.exists(input_value):  # If input is a file
        with open(input_value, "r") as file:
            urls = [ensure_full_url(line.strip()) for line in file if line.strip() and validators.url(ensure_full_url(line.strip()))]
        if not urls:
            return
    else:  # Single URL
        if validators.url(ensure_full_url(input_value)):
            urls.append(ensure_full_url(input_value))
        else:
            return

    os.makedirs(output_folder, exist_ok=True)

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust worker count as needed
        futures = {executor.submit(capture_screenshot, url, output_folder): url for url in urls}
        for future in as_completed(futures):
            future.result()  # Ensures all threads complete


# GUI for user interaction
def run_gui():
    """ Launches GUI for selecting input and output folder """
    def start_screenshot_thread():
        """ Runs screenshot capturing in a separate thread to keep GUI responsive """
        url_or_file = url_entry.get()
        output_folder = folder_entry.get()
        if not url_or_file or not output_folder:
            messagebox.showwarning("Warning", "Please enter a valid URL or file and select an output folder.")
            return

        # Disable button to prevent multiple clicks
        capture_button.config(state=tk.DISABLED)
        status_label.config(text="Processing... Please wait.")

        def run_capture():
            capture_screenshots(url_or_file, output_folder)
            root.after(0, on_screenshot_complete)

        threading.Thread(target=run_capture, daemon=True).start()

    def on_screenshot_complete():
        """ Re-enable GUI elements after processing """
        capture_button.config(state=tk.NORMAL)
        status_label.config(text="Screenshots captured successfully!")
        messagebox.showinfo("Success", "Screenshots captured successfully!")

    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            url_entry.delete(0, tk.END)
            url_entry.insert(0, filename)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder)

    root = tk.Tk()
    root.title("Fast Firefox Screenshot Tool")
    root.geometry("500x250")

    tk.Label(root, text="Enter URL or Select File:").pack(pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)
    tk.Button(root, text="Browse File", command=browse_file).pack(pady=5)

    tk.Label(root, text="Select Output Folder:").pack(pady=5)
    folder_entry = tk.Entry(root, width=50)
    folder_entry.pack(pady=5)
    tk.Button(root, text="Browse Folder", command=browse_folder).pack(pady=5)

    capture_button = tk.Button(root, text="Capture Screenshots", command=start_screenshot_thread)
    capture_button.pack(pady=10)

    status_label = tk.Label(root, text="", fg="blue")
    status_label.pack(pady=5)

    root.mainloop()


# Run CLI or GUI mode
if __name__ == "__main__":
    if len(sys.argv) == 3:
        capture_screenshots(sys.argv[1], sys.argv[2])
    else:
        run_gui()
