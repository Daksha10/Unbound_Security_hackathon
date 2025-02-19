# 🚀 Unbound Chat Routing System  

## 📌 Overview  
This project is a **smart AI-powered chat routing system** that dynamically directs user queries to different **LLM (Large Language Model) providers** based on **regex-based routing rules** stored in a PostgreSQL database. It features:  
✅ **Regex-based Routing** – Dynamically reroute prompts based on patterns.  
✅ **Admin Portal** – Manage regex rules via a web UI.  
✅ **File Upload Handling** – Process PDF uploads with special routing policies.  
✅ **Interactive Chat UI** – Simple web-based chat for prompt testing.  

---

## 🛠️ Tech Stack  

| Component  | Technology |
|------------|------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Flask) |
| **Database** | PostgreSQL |
| **LLM Providers(stub LLMs)** | OpenAI, Anthropic, etc. |

---

## ⚙️ System Architecture  

```plaintext
┌────────────────────────────────────┐
│  🌍 Web-based Chat UI (Frontend)   │
│  - Users enter prompts             │
│  - File upload support             │
└───────────────┬────────────────────┘
                │
                ▼
┌────────────────────────────────────┐
│  🚀 Flask Backend                  │
│  - Routes requests                 │
│  - Applies regex-based routing     │
│  - Interacts with PostgreSQL        │
│  - Connects to LLM providers        │
└───────────────┬────────────────────┘
                │
                ▼
┌────────────────────────────────────┐
│  🗄️ PostgreSQL Database             │
│  - Stores regex-based routing rules │
│  - Maps models & special policies   │
└───────────────-────────────────────┘
```

---

## 🚀 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Daksha10/Unbound_Security_hackathon.git
cd Unbound_Security_hackathon
```

### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up PostgreSQL Database  
Ensure **PostgreSQL** is installed and running. Then:  
- **Create a new database**:  
  ```sql
  CREATE DATABASE chat_routing;
  ```
- **Update your environment variables (`.env`)**:  
  ```
  DB_NAME=chat_routing
  DB_USER=your_username
  DB_PASSWORD=your_password
  DB_HOST=localhost
  DB_PORT=5432
  ```

### 4️⃣ Run the Flask Server  
```bash
python app.py
```
By default, the Flask backend will run on `http://127.0.0.1:5000/`.

### 7️⃣ Run the Frontend  
- Open `http://127.0.0.1:5000/` in your browser.

---

## 🎯 Usage Details  

### ✅ **1. Chat Interface**  
- Select a **model provider** (e.g., OpenAI, Anthropic).  
- Enter a **text prompt** and hit **Send**.  
- The backend routes your query to the **best-matched model** based on regex rules.  

### ✅ **2. Regex-Based Routing**  
- The backend **checks PostgreSQL** for matching regex patterns.  
- If a match is found, **reroute the request** to a specific LLM model.  
- If no match is found, **default to the primary model**.

### ✅ **3. Admin Portal (Regex Management)**  
- **Add, edit, delete** regex-based routing rules.  
- Assign each rule to a **specific LLM model**.

### ✅ **4. File Upload Handling**  
- Upload **PDF files** directly from the chat UI.  
- The system routes file processing requests to **special models**.  
- Example: PDFs can be automatically assigned to **Claude** instead of GPT.

---

## 🎥 Demo Video  
📌 [Click here to watch the demo](#) 

--- 
