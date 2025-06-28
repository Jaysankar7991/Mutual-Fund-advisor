import streamlit as st
from kite_mcp_client import KiteMCPClient


# Title and intro
st.title("AI-Powered Equity & Debt Advisor")
st.write("Enter your investment preferences to get a personalized recommendation.")

# Initialize Kite MCP client
client = KiteMCPClient()

# --- Kite Login Section ---
with st.expander("Kite Login", expanded=True):
    if st.button("Login to Kite"):
        login_url = client.login()
        st.markdown(f"[Click here to log in to Zerodha 🪁]({login_url})", unsafe_allow_html=True)
        st.info("Once logged in, your Kite session will be active in this VS Code environment.")

# --- Investment Preferences ---
st.header("Investment Preferences")
def accept_user_input():
    age = st.number_input("Enter your age", min_value=18, max_value=100, step=1)
    risk = st.selectbox("Select your risk appetite", ["Low", "Medium", "High"])
    amount = st.number_input("Investment Amount (₹)", min_value=500, step=100)
    frequency = st.selectbox("Investment Frequency", ["One-time", "Monthly", "Quarterly"])
    return age, risk, amount, frequency

age, risk, amount, freq = accept_user_input()

# --- Get Recommendation Button ---
if st.button("Get Recommendation"):
    prompt = f"""
    Based on the following investor profile such as age {age}, risk appetite {risk},
    amount ₹{amount} and investment frequency {freq}, suggest an ideal allocation
    between equity and debt. Provide a brief recommendation.
    """

    with st.spinner("Querying Kite MCP..."):
        try:
            result = client.query(prompt)
            st.success("AI Recommendation:")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")
