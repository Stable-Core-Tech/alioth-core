![Alioth](/public/alioth.jpg)

Twitter:https://x.com/Alioth_system

Whitepaper:https://persons-organization.gitbook.io/alioth-system

# Alioth Core

[![Twitter Follow](https://img.shields.io/twitter/follow/Alioth_system?style=social)](https://x.com/Alioth_system)
[![GitHub stars](https://img.shields.io/github/stars/Stable-Core-Tech/alioth-core?style=social)](https://github.com/Stable-Core-Tech/alioth-core)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Abstract

The Alioth System is an innovative AI-powered platform designed to revolutionize data analysis and decision-making in the blockchain ecosystem. By leveraging advanced artificial intelligence technologies, Alioth aims to provide accurate data direction and valuable insights from vast blockchain datasets.



### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Stable-Core-Tech/alioth-core.git
cd alioth-core
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Build the frontend:
```bash
npm run build
```

## Configuration

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/alioth

# API Configuration
API_KEY=your_api_key
API_URL=http://localhost:8000

# Blockchain Configuration
BLOCKCHAIN_NODE_URL=https://your-node-url
BLOCKCHAIN_NETWORK=ethereum

# AI Configuration
MODEL_PATH=/path/to/models
RISK_THRESHOLD=0.7
```

## Usage

### Starting the Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

### Starting the Frontend Development Server

## API Documentation

### Risk Assessment

```python
POST /api/v1/risk-assessment

{
    "token_data": [
        {"price": 100},
        {"price": 102},
        {"price": 98}
    ]
}
```

### Portfolio Optimization

```python
POST /api/v1/optimize-portfolio

{
    "portfolio": {
        "BTC": 1.5,
        "ETH": 10.0
    },
    "risk_tolerance": 0.7
}
```


### Running Tests

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend
npm test
```


## Security

For security concerns, please email security@alioth-system.site

## Support

For support questions, please use [GitHub Issues](https://github.com/Stable-Core-Tech/alioth-core/issues)
