# TaxIQ 💼

An AI-powered tax return generator built with Python and Streamlit.

## What it does
- Upload your W-2 or 1099 and AI extracts your tax information automatically
- Fill out a simple form with your tax details
- Calculates your estimated refund or amount owed
- Generates a downloadable tax return PDF

## Built with
- Python
- Streamlit
- Anthropic Claude API
- ReportLab

## How to run
1. Clone the repository
2. Install dependencies: `pip install streamlit anthropic python-dotenv reportlab`
3. Add your Anthropic API key to a `.env` file: `ANTHROPIC_API_KEY=your-key-here`
4. Run: `streamlit run app.py`

## Note
TaxIQ is for educational purposes only and should not be used as official tax advice.