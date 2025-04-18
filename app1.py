import streamlit as st
import pandas as pd

# Function to calculate fee and breakdown
def calculate_fee_with_breakdown(amount):
    breakdown = []
    fee = 0

    if amount > 50000:
        breakdown.append(("₹1 – ₹5,000", 5000, "20%", 5000 * 0.20))
        breakdown.append(("₹5,001 – ₹20,000", 15000, "10%", 15000 * 0.10))
        breakdown.append(("₹20,001 – ₹50,000", 30000, "8%", 30000 * 0.08))
        slab_amount = amount - 50000
        breakdown.append((f"₹50,001 – ₹{amount:,}", slab_amount, "5%", slab_amount * 0.05))
        fee = sum(row[3] for row in breakdown)

    elif amount > 20000:
        breakdown.append(("₹1 – ₹5,000", 5000, "20%", 5000 * 0.20))
        breakdown.append(("₹5,001 – ₹20,000", 15000, "10%", 15000 * 0.10))
        slab_amount = amount - 20000
        breakdown.append((f"₹20,001 – ₹{amount:,}", slab_amount, "8%", slab_amount * 0.08))
        fee = sum(row[3] for row in breakdown)

    elif amount > 5000:
        breakdown.append(("₹1 – ₹5,000", 5000, "20%", 5000 * 0.20))
        slab_amount = amount - 5000
        breakdown.append((f"₹5,001 – ₹{amount:,}", slab_amount, "10%", slab_amount * 0.10))
        fee = sum(row[3] for row in breakdown)

    else:
        breakdown.append((f"₹1 – ₹{amount:,}", amount, "20%", amount * 0.20))
        fee = sum(row[3] for row in breakdown)

    return round(fee, 2), round(fee / 3, 2), breakdown

# Streamlit config
st.set_page_config(
    page_title="Advocate Fee - Munsiff Court Kerala",
    page_icon="⚖️",
    layout="centered"
)

# Sidebar
with st.sidebar:
    st.header("📌 About")
    st.markdown("""
    **Creator:** Rahul K  
    **Tool Purpose:**  
    Calculates advocate fees for  
    **Money Suits** and **Execution Petitions**  
    in **Munsiff Courts (Kerala)** using slab-based rules.
    """)

# App Title
st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>⚖️ Advocate Fee Calculator</h1>
    <h4 style='text-align: center; color: #4A4A4A;'>Munsiff Court – Money Suits & Execution Petitions</h4>
""", unsafe_allow_html=True)

# Input
amount = st.number_input("Enter the Claim Amount (₹):", min_value=1, step=100)

# Output
if amount:
    total_fee, ep_fee, breakdown = calculate_fee_with_breakdown(amount)

    st.markdown("### 🧾 Fee Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💼 Fee in Suit (Total)", f"₹{total_fee:,.2f}")
    with col2:
        st.metric("📄 Fee in Execution Petition (1/3)", f"₹{ep_fee:,.2f}")

    st.markdown("### 📊 Slab-Wise Fee Breakdown")
    df = pd.DataFrame(breakdown, columns=["Slab", "Amount in Slab", "Rate", "Fee"])
    df["Amount in Slab"] = df["Amount in Slab"].apply(lambda x: f"₹{x:,.2f}")
    df["Fee"] = df["Fee"].apply(lambda x: f"₹{x:,.2f}")
    st.table(df)

    st.info("✅ Calculated as per official slab structure applicable in Kerala Munsiff Courts.")

