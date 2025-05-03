import streamlit as st
import re
import secrets
import string

def check_password_strength(password):
    """Evaluate password strength and provide feedback"""
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Should be at least 8 characters long (12+ recommended)")
    
    # Upper & Lowercase Check
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    if has_upper and has_lower:
        score += 1
    else:
        feedback.append("❌ Should include both uppercase and lowercase letters")
    
    # Digit Check
    has_digit = bool(re.search(r"\d", password))
    if has_digit:
        score += 1
    else:
        feedback.append("❌ Should include at least one number (0-9)")
    
    # Special Character Check
    has_special = bool(re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?/~`-]", password))
    if has_special:
        score += 1
    else:
        feedback.append("❌ Should include at least one special character")
    
    # Common password check
    common_passwords = ["password", "123456", "qwerty", "letmein", "welcome"]
    if password.lower() in common_passwords:
        score = 0
        feedback.append("❌ This is a commonly used password - choose something more unique")
    
    # Sequential characters check (e.g., "1234", "abcd")
    if re.search(r"(.)\1{2,}", password) or re.search(r"(123|abc|qwe|asd|zxc)", password.lower()):
        score = max(0, score - 1)
        feedback.append("❌ Avoid sequential or repeated characters")
    
    return score, feedback

def generate_strong_password(length=16):
    """Generate a strong random password"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+{}[]:;<>,.?/~`"
    while True:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        score, _ = check_password_strength(password)
        if score >= 4:  # Ensure it meets our strong criteria
            return password

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")

# Custom CSS
st.markdown("""
<style>
.stProgress > div > div > div > div {
    background-color: #4CAF50;
}
.weak {
    color: #FF5722;
}
.moderate {
    color: #FFC107;
}
.strong {
    color: #4CAF50;
}
.feedback-item {
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔐 Password Strength Meter")
st.write("Check how strong your password is and get suggestions for improvement")

# Password input
col1, col2 = st.columns([3, 1])
with col1:
    password = st.text_input("Enter your password:", type="password", placeholder="Type or paste your password here")
with col2:
    if st.button("Generate Strong Password"):
        generated_pw = generate_strong_password()
        st.session_state.generated_password = generated_pw
        password = generated_pw

if 'generated_password' in st.session_state:
    st.text_input("Generated password (copy this):", 
                 value=st.session_state.generated_password, 
                 key="display_generated")

if password:
    score, feedback = check_password_strength(password)
    
    # Visual strength indicator
    st.subheader("Password Strength")
    strength_labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Moderate",
        4: "Strong",
        5: "Very Strong"
    }
    
    strength_class = "weak" if score <= 2 else "moderate" if score <= 4 else "strong"
    st.markdown(f"### <span class='{strength_class}'>{strength_labels.get(score, 'Unknown')}</span>", 
                unsafe_allow_html=True)
    st.progress(score/5)
    
    # Feedback section
    if score >= 4:
        st.success("✅ Excellent! This password meets all security requirements.")
    else:
        st.subheader("Recommendations to improve:")
        for item in feedback:
            st.markdown(f"<div class='feedback-item'>{item}</div>", unsafe_allow_html=True)
    
    # Additional security checks
    st.subheader("Security Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Length", len(password))
    with col2:
        st.metric("Character Types", 
                 len(set(re.findall(r"\w", password))))
    with col3:
        st.metric("Entropy Score", 
                 f"{len(password) * 4:.0f} bits" if len(password) else "0 bits")
    
    # Password hashing demonstration (educational)
    st.markdown("---")
    st.caption("ℹ️ Note: This tool evaluates password strength locally in your browser. "
              "For real security, passwords should always be hashed (not stored in plain text).")
else:
    st.info("ℹ️ Enter a password to check its strength")

# Additional information
with st.expander("What makes a strong password?"):
    st.write("""
    - **Length**: At least 12 characters (the longer the better)
    - **Complexity**: Mix of uppercase, lowercase, numbers, and special characters
    - **Unpredictability**: Avoid common words, phrases, or patterns
    - **Uniqueness**: Don't reuse passwords across different accounts
    """)
    
    st.write("Consider using a password manager to generate and store strong passwords securely.")