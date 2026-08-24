# WiseBuyer AI

WiseBuyer AI is a product comparison and purchase-assistance chatbot built with Flask and a large language model API.

The idea behind the project is simple: instead of searching through several product pages and trying to compare everything manually, the user can interact with WiseBuyer and get product information, comparisons, reasoning, and purchase recommendations from one interface.

The project currently uses a local product database along with Groq's API for AI-generated responses.

## Features

WiseBuyer provides several ways to look at a product before making a purchase:

* Full product specifications
* Product comparison
* AI-based reasoning
* Social proof analysis
* Sentiment analysis
* Price and resale prediction
* Final purchase recommendation
* Financial advice
* Support for adding or analysing a new product

The application is designed so that the user can select a product category, choose a product, and then decide what kind of analysis they want.

## How It Works

The basic flow is:

```text
User
  ↓
WiseBuyer Web Interface
  ↓
Product Selection
  ↓
Selected Analysis
  ↓
Local Product Database + AI Model
  ↓
Result / Recommendation
```

Product information is stored locally in `data/products.json`. AI-related reasoning is handled through the Groq API.

## Technologies Used

### Backend

* Python
* Flask

### AI

* Groq API
* Llama 3.1 8B Instant

### Frontend

* HTML
* CSS
* JavaScript

### Data

* JSON-based local product database

### Other

* Requests
* python-dotenv
* Git and GitHub

## Project Structure

```text
WiseBuyer-AI/
│
├── app.py
├── wisebuyer.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   └── products.json
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    ├── index.html
    ├── result.html
    └── financial_result.html
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/prithvi2216999/WiseBuyer-AI.git
cd WiseBuyer-AI
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, the project can also be run directly with the Python executable inside the virtual environment:

```powershell
.\venv\Scripts\python.exe app.py
```

### 4. Install the dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a file named:

```text
.env
```

in the project root.

Add:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not upload the `.env` file to GitHub.

The `.gitignore` file already excludes it from Git.

### 6. Start WiseBuyer

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## API Key Security

The Groq API key is loaded from an environment variable instead of being stored directly in the source code.

The project uses:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

The `.env` file is excluded through `.gitignore`.

Never commit or publish an API key in the repository.

## Current Limitations

WiseBuyer currently depends on the quality and completeness of the product information available in its local JSON database.

AI-generated recommendations should also be treated as decision support rather than absolute purchasing advice. Prices, availability, resale values, and product specifications can change over time.

## Future Improvements

Some possible improvements for future versions include:

* Connecting to live product and price data
* Adding more product categories
* Improving product recommendation logic
* Adding user preference and budget profiles
* Adding price tracking
* Adding product availability checking
* Improving recommendation evaluation
* Adding a larger and more structured product database
* Deploying the application as a public web service

## Author

**Prithvi Raj**

GitHub:
https://github.com/prithvi2216999
