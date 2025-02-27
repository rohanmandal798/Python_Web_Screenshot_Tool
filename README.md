## **📸 Fast Firefox Screenshot Tool**  
*A multithreaded tool for capturing website screenshots using Selenium and Firefox WebDriver.*  


---

### **🔹 Features**  
✅ Supports both **CLI** and **GUI** mode  
✅ Captures full-page screenshots using **Firefox WebDriver**  
✅ **Multithreaded execution** for fast processing  
✅ Supports **single URLs** and **bulk URL input from a file**  
✅ Saves failed attempts in a **log file**  
✅ **User-friendly GUI** built with **Tkinter**  

---

## **📥 Installation**  

### **🔹 Prerequisites**  
1. Install **Python 3.9+**  
2. Install required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Download **Geckodriver** (required for Firefox WebDriver):  
   - [Download Geckodriver](https://github.com/mozilla/geckodriver/releases)  
   - Extract and place it in the project folder or system path  

---

## **🚀 Usage**  

### **🔹 CLI Mode**  
Run the script directly from the terminal:  
#### **Capture a single website screenshot**  
```bash
python Screenshot_Tool.py "https://example.com" "output_folder/"
```
#### **Capture multiple screenshots from a file**  
```bash
python Screenshot_Tool.py "urls.txt" "output_folder/"
```
*(Ensure `urls.txt` contains one URL per line.)*  

---

### **🔹 GUI Mode**  
1️⃣ Run the GUI:  
   ```bash
   python Screenshot_Tool.py
   ```  
2️⃣ Enter a **URL or select a text file** with multiple URLs  
3️⃣ Choose an **output folder**  
4️⃣ Click **"Capture Screenshots"**  

---

## **🧪 Running Tests**  
Unit tests are provided in the `tests/` directory. To run all tests:  
```bash
python -m unittest discover tests
```

## **🔧 Known Issues & Future Enhancements**  
### **❌ Known Issues**  
- Some sites with **CAPTCHAs** or **Cloudflare protection** may not be captured  
- Headless mode might fail on some sites with **JavaScript-heavy content**  

### **🚀 Future Enhancements**  
✅ Support for **Chrome WebDriver**  
✅ Add **auto-retry** for failed screenshots  
✅ Implement **parallel processing with multiprocessing**  

 