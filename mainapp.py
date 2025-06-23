
import os
import streamlit as st
import openai

# Set your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.title("AI-Powered Equity & Debt Advisor")
st.write("Enter your investment preferences to get a personalized recommendation.")

# Accepting user input
def accept_user_input():
    age = st.number_input("Enter your age", min_value=18, max_value=100, step=1)
    risk = st.selectbox("Select your risk appetite", ["Low", "Medium", "High"])
    amount = st.number_input("Investment Amount (₹)", min_value=500, step=100)
    frequency = st.selectbox("Investment Frequency", ["One-time", "Monthly", "Quarterly"])
    return age, risk, amount, frequency


age, risk, amount, freq = accept_user_input()

# When submit is clicked
if st.button("Get Recommendation"):
    prompt = f"""
    Based on the following investor profile such as age {age},-risk appetite-{risk}, amount- ₹{amount} and Investment frequency-{freq}, suggest an ideal allocation between equity and debt:
    Provide a brief recommendation in 3-4 lines.
    """

    with st.spinner("Generating advice..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            advice = response['choices'][0]['message']['content']
            st.success("AI Recommendation:")
            st.write(advice)
        except Exception as e:
            st.error(f"Error: {str(e)}")
