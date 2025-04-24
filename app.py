import streamlit as st
import string
import random
import re
import matplotlib.pyplot as plt

# ------------------------------
# 🔴 Blacklisted passwords
blacklist = ["password", "123456", "admin", "12345678", "qwerty", "password123", "abc123", "letmein", "111111"]

# ------------------------------
# 🔍 Password Strength & Analysis
def analyze_password(password):
    analysis = {
        "length": len(password),
        "uppercase": sum(1 for c in password if c.isupper()),
        "lowercase": sum(1 for c in password if c.islower()),
        "digits": sum(1 for c in password if c.isdigit()),
        "symbols": sum(1 for c in password if c in string.punctuation)
    }

    score = 0
    tips = []

    if password.lower() in blacklist:
        return 10, "❌ Weak", analysis, ["Password is blacklisted. Use something original."]

    if analysis["length"] >= 8:
        score += 25
    else:
        tips.append("Increase length to at least 8 characters.")

    if analysis["uppercase"] > 0: score += 15
    else: tips.append("Add uppercase letters.")

    if analysis["lowercase"] > 0: score += 15
    else: tips.append("Add lowercase letters.")

    if analysis["digits"] > 0: score += 15
    else: tips.append("Include digits.")

    if analysis["symbols"] > 0: score += 20
    else: tips.append("Add symbols like !, @, #.")

    if re.search(r'(.)\1{2,}', password) or re.search(r'123|abc|qwerty', password.lower()):
        tips.append("Avoid repeating/sequential patterns.")

    if score < 40:
        verdict = "❌ Weak"
    elif score < 70:
        verdict = "⚠️ Moderate"
    else:
        verdict = "✅ Strong"

    return min(score, 100), verdict, analysis, tips

# ------------------------------
# 🔄 Strong Password Generator
def generate_password(length=12, upper=True, lower=True, digits=True, symbols=True):
    characters = ""
    if upper: characters += string.ascii_uppercase
    if lower: characters += string.ascii_lowercase
    if digits: characters += string.digits
    if symbols: characters += string.punctuation
    if not characters: return "⚠️ Select at least one option."

    return ''.join(random.choice(characters) for _ in range(length))

# ------------------------------
# 📊 Character Pie Chart
def plot_characters(analysis):
    labels = ['Uppercase', 'Lowercase', 'Digits', 'Symbols']
    sizes = [analysis['uppercase'], analysis['lowercase'], analysis['digits'], analysis['symbols']]
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

# ------------------------------
# 🌐 UI
st.set_page_config(page_title="PassShield Pro", page_icon="🛡️", layout="centered")
st.title("🛡️ PassShield Pro - Password Strength & Security Analyzer")
st.markdown("Secure your digital identity with password insights, feedback, and generation.")

# ------------------------------
# Password Input
st.subheader("🔐 Analyze Your Password")
password = st.text_input("Enter a password to check", type="password")

if st.button("Check Password"):
    if password:
        score, verdict, analysis, tips = analyze_password(password)

        st.markdown(f"### Strength: {verdict}")
        st.progress(score)
        st.write(f"**Length:** {analysis['length']} characters")
        st.success("Character Analysis (Chart below)")
        plot_characters(analysis)

        if tips:
            st.warning("Suggestions:")
            for t in tips:
                st.markdown(f"- {t}")

        # 💡 Security Tips
        st.markdown("#### 💡 Security Tips")
        if verdict == "❌ Weak":
            st.error("Avoid dictionary words, short passwords, or common patterns.")
        elif verdict == "⚠️ Moderate":
            st.info("You're getting there! Consider adding more variety to your password.")
        else:
            st.success("Awesome! Your password is strong.")

    else:
        st.error("Please enter a password.")

# ------------------------------
st.divider()
st.subheader("🎲 Generate a Secure Password")

with st.form("generate"):
    col1, col2 = st.columns(2)
    with col1:
        length = st.slider("Length", 8, 24, 12)
        upper = st.checkbox("Uppercase", True)
        digits = st.checkbox("Digits", True)
    with col2:
        lower = st.checkbox("Lowercase", True)
        symbols = st.checkbox("Symbols", True)

    generate_btn = st.form_submit_button("Generate Password")

if generate_btn:
    new_pass = generate_password(length, upper, lower, digits, symbols)
    st.code(new_pass, language="text")
    st.caption("Copy and save this password securely!")

# ------------------------------
st.markdown("---")
st.caption("🚀 Built with 🛡️ by Kiran | Unique. Secure. Powerful.")


