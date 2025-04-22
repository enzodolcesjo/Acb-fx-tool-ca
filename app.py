import streamlit as st
import pandas as pd
import acb_fx_calculator

st.title("ACB & FX Gain Calculator (Canada)")

st.sidebar.header("Upload Required Files")
trades_file = st.sidebar.file_uploader("Upload Trades File", type=["xlsx"])
opening_file = st.sidebar.file_uploader("Upload Opening Positions File", type=["xlsx"])
fx_file = st.sidebar.file_uploader("Upload FX Rates File", type=["xlsx"])

if trades_file and opening_file and fx_file:
    st.success("All files uploaded! Click below to process.")
    if st.button("Run ACB & FX Calculation"):
        trades_df = pd.read_excel(trades_file)
        opening_df = pd.read_excel(opening_file)
        fx_df = pd.read_excel(fx_file)
        result = acb_fx_calculator.process(trades_df, opening_df, fx_df)
        st.subheader("Summary")
        st.dataframe(pd.DataFrame(result["summary"]))
        st.subheader("Audit Trail")
        st.dataframe(pd.DataFrame(result["audit"]))
        with pd.ExcelWriter("summary_audit.xlsx", engine="openpyxl") as writer:
            pd.DataFrame(result["summary"]).to_excel(writer, sheet_name="Summary", index=False)
            pd.DataFrame(result["audit"]).to_excel(writer, sheet_name="AuditTrail", index=False)
        with open("summary_audit.xlsx", "rb") as f:
            st.download_button("Download Results", f, file_name="summary_audit.xlsx")
