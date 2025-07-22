# 💼 SmartInvest Basket

*SmartInvest Basket* is a **personalized stock investment platform** that crafts tailored stock baskets based on a user's **income level** and **risk appetite** (High / Low). Each basket is **diversified across multiple sectors and market caps**, aiming to balance growth potential with risk.

Our algorithm uses a **composite score** combining 📘 **fundamental analysis**, 📉 **technical indicators**, and 📰 **news sentiment** to rank and select stocks — enabling **data-driven investment decisions**.

---

## 🧠 Key Features

- 🔍 **Smart Basket Generation**  
  Tailored recommendations based on:
  - 💰 Income Input
  - ⚖️ Risk Appetite (High / Low)

- 📈 **Diversified Exposure**  
  Across:
  - Largecap, Midcap, Smallcap
  - Sectoral themes (e.g., IT, Healthcare, Auto)

- 📊 **Intelligent Stock Selection**  
  Driven by:
  - 📘 Fundamental Metrics (P/E, EPS, etc.)
  - 📉 Technical Indicators (like RSI)
  - 📰 Real-time News Sentiment Scoring

- 🔐 **Secure User Authentication**  
  Seamless Login / Registration with encryption

---

## 🚀 Tech Stack

### 🖥️ Frontend
- ⚛️ **React.js** – Dynamic & modular UI
- 🎨 **Tailwind CSS** – Clean and responsive styling

### 🧠 Backend
- 🟩 **Node.js + Express.js** – REST APIs & auth logic
- 🍃 **MongoDB** – NoSQL database for users and baskets

### 🐍 Python (Data & Scraping)
- 🧮 **Pandas** – Data cleaning & transformation
- ➕ **NumPy** – Financial computations
- 🌐 **Requests / BeautifulSoup** – Scraping stock info from the web

### 🔌 Integrations
- 🧠 Custom Python scripts for:
  - Live stock price fetching
  - Basket generation logic
- 🔄 API endpoints to serve computed data to the UI

---

## 📸 Screenshots

| 🖼️ Page | Preview |
|--------|---------|
| 🔐 Login | ![Login](./screenshots/Screenshot%202025-04-08%20130854.png) |
| 📝 Register | ![Register](./screenshots/Screenshot%202025-04-08%20132246.png) |
| 📊 Dashboard | ![Dashboard](./screenshots/Screenshot%202025-04-08%20130943.png) |
| 📈 Basket Overview | ![Basket](./screenshots/Screenshot%202025-04-08%20130955.png) |
| 🧾 Stock Details | ![Details](./screenshots/Screenshot%202025-04-08%20131016.png) |
| 📉 Growth Graph | ![Graph](./screenshots/Screenshot%202025-04-08%20132900.png) |

---

## 🧪 How to Run Locally

```bash
# 1️⃣ Clone the repository
git clone https://github.com/yourusername/smartinvest-basket.git

# 2️⃣ Navigate to the project folder
cd smartinvest-basket

# 3️⃣ Install project dependencies
npm install

# 4️⃣ Run the development server (client + server concurrently)
npm run dev
