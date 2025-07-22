# 💼 SmartInvest Basket

**SmartInvest Basket** is a personalized stock investment tool that generates optimized stock baskets tailored to an individual's income and risk profile (High/Low). It empowers users to make **data-driven investment decisions** through diversified portfolios based on themes and sectors.



---

## 🧠 Key Features

- 🔍 **Smart Basket Generation** based on:
  - Income input
  - Risk appetite (High/Low)
- 📈 **Diversification** across:
  - Largecap, Midcap, Smallcap, Sector-based themes (IT, Healthcare, Auto, etc.)
- 📊 **Data-Driven Decisions** using:
  - 📘 Fundamental Analysis
  - 📉 Technical Indicators
  - 📰 News Sentiment Scoring
- 📂 **Detailed Stock View**:
  - Company info, current price, 52-week range
- 🔐 User Authentication: Secure login & registration

---

## 🚀 Tech Stack

## 🚀 Tech Stack

### 🖥️ Frontend:
- **React.js** – Component-based dynamic interface
- **Tailwind CSS** – Modern and responsive styling

### 🧠 Backend:
- **Node.js + Express.js** – API server and user authentication
- **MongoDB** – Storing user info, preferences, and saved baskets

### 🐍 Python (for Data Handling & Scraping):
- **Pandas** – Data preprocessing and filtering
- **NumPy** – Numerical computation
- **Requests / BeautifulSoup** – Web scraping for live stock prices and metrics

### 📡 Integrations:
- Custom Python scripts for:
  - Stock price fetching
  - Basket generation logic
- Express routes to fetch and display computed results on the frontend

---

## 📸 Screenshots

### 🔐 Login Page
![Login](./screenshots/Screenshot%202025-04-08%20130854.png)

### 📝 Registration Page
![Register](./screenshots/Screenshot%202025-04-08%20132246.png)

### 📊 Dashboard
![Dashboard](./screenshots/Screenshot%202025-04-08%20130943.png)

### 📈 Basket Overview
![Basket Overview](./screenshots/Screenshot%202025-04-08%20130955.png)

### 🧾 Stock Details
![Stock Details](./screenshots/Screenshot%202025-04-08%20131016.png)

### 📉 Growth Graph
![Graph](./screenshots/Screenshot%202025-04-08%20132900.png)

---

## 🧪 How to Use

```bash
# Clone the repository
git clone https://github.com/yourusername/smartinvest-basket.git

# Navigate to the project folder
cd smartinvest-basket

# Install dependencies for both client and server
npm install

# Run the development server
npm run dev
