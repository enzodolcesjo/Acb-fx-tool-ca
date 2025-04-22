# ACB & FX Gain Calculator (Canada)

This Streamlit-based web app helps Canadian investors calculate Adjusted Cost Base (ACB) and Foreign Exchange (FX) gains/losses for capital gains tax reporting.

## Features

- Upload Excel trade data, opening positions, and FX rates
- Computes:
  - ACB per stock (CAD)
  - Capital gains/losses (CAD)
  - FX gains/losses for foreign-denominated stocks
- Outputs:
  - Summary report
  - Detailed audit trail
  - Downloadable Excel file

## Usage

1. Upload the following Excel files:
   - `Trades_2024.xlsx` – trade history for the current year
   - `Opening_Positions.xlsx` – ACB and FX balance at year start
   - `FX_2023.xlsx` – FX rates for opening balances

2. Click **"Run ACB & FX Calculation"** to view the report.

3. Use the **Download Results** button to save results to Excel.

## Sample File Structure

```
acb_fx_tool_gui/
├── app.py
├── requirements.txt
└── modules/
    └── acb_fx_calculator.py
```

## Disclaimer

This tool is for educational and personal finance purposes. Always consult a tax professional for CRA reporting and compliance.

## License

MIT License
