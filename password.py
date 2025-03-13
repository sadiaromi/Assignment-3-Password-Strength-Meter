import streamlit as st
import re
import string
import random
import time

# Set page config
st.set_page_config(
    page_title="Password Strength Meter & Generator",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS 
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
        padding: 20px;
    }
    
    /* Header styling */
    h1 {
        color: #1e3a8a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    h2 {
        color: #1e3a8a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
        margin-top: 30px;
    }
    
    h3 {
        color: #334155;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    /* Card styling */
    .css-card {
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        height: 15px !important;
        border-radius: 10px !important;
    }
    
    /* Code block styling */
    .css-password-display {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        color: #334155;
        overflow-x: auto;
        white-space: nowrap;
        margin-top: 10px;
        width: 100%;
    }
    
    /* Checkbox styling */
    .stCheckbox label p {
        font-size: 14px !important;
    }
    
    /* Slider styling */
    .stSlider {
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    
    /* Divider styling */
    hr {
        margin-top: 30px !important;
        margin-bottom: 30px !important;
        border-top: 1px solid #e2e8f0 !important;
    }
    
    /* Feedback item styling */
    .feedback-item {
        padding: 8px 12px;
        margin-bottom: 8px;
        border-radius: 6px;
        background-color: #f8fafc;
        border-left: 4px solid #ef4444;
    }
    
    .feedback-success {
        border-left: 4px solid #10b981;
        background-color: #f0fdf4;
    }
    
    /* Strength indicator styling */
    .strength-very-weak {
        color: #b91c1c;
        font-weight: 600;
    }
    
    .strength-weak {
        color: #ea580c;
        font-weight: 600;
    }
    
    .strength-moderate {
        color: #ca8a04;
        font-weight: 600;
    }
    
    .strength-strong {
        color: #16a34a;
        font-weight: 600;
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state for generated password
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""

# Main heading
st.markdown('<h1>Password Strength Meter and Generator</h1>', unsafe_allow_html=True)

# Common passwords list
common_passwords = [
    "password", "123456", "qwerty", "admin", "welcome", 
    "123456789", "12345678", "abc123", "password1", "1234567"
]

# Function to generate a random password
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    characters = ""
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    if not characters:
        return "Please select at least one character type"
    
    return ''.join(random.choice(characters) for _ in range(length))

# Password Strength Checker Section
st.markdown('<div class="css-card">', unsafe_allow_html=True)
st.markdown('<h2>📊 Check Password Strength</h2>', unsafe_allow_html=True)

# Password input with option to use generated password
if st.session_state.generated_password and st.button("Use Generated Password", key="use_generated"):
    password = st.session_state.generated_password
else:
    password = ""

password = st.text_input("Enter your password:", value=password, type="password")

if password:
    # Calculate strength score (0-100)
    score = 0
    feedback = []
    
    # Check length
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
        feedback.append("❗ Make your password longer (12+ characters recommended)")
    else:
        feedback.append("❌ Password is too short (minimum 8 characters recommended)")
    
    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        feedback.append("❌ Add uppercase letters")
    
    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 15
    else:
        feedback.append("❌ Add lowercase letters")
    
    # Check for numbers
    if re.search(r'\d', password):
        score += 15
    else:
        feedback.append("❌ Add numbers")
    
    # Check for special characters
    if re.search(r'[' + re.escape(string.punctuation) + ']', password):
        score += 15
    else:
        feedback.append("❌ Add special characters (!@#$%^&*)")
    
    # Check for common passwords
    if password.lower() in common_passwords:
        score = 0
        feedback = ["❌ This is a commonly used password and very insecure"]
    
    # Determine strength category
    if score >= 80:
        strength = "Strong"
        strength_class = "strength-strong"
        color = "#16a34a"
    elif score >= 60:
        strength = "Moderate"
        strength_class = "strength-moderate"
        color = "#ca8a04"
    elif score >= 30:
        strength = "Weak"
        strength_class = "strength-weak"
        color = "#ea580c"
    else:
        strength = "Very Weak"
        strength_class = "strength-very-weak"
        color = "#b91c1c"
    
    # Display strength meter with animation
    st.markdown(f'<h3>Password Strength: <span class="{strength_class}">{strength}</span></h3>', unsafe_allow_html=True)
    
    # Custom progress bar with animation
    progress_bar = st.progress(0)
    for i in range(score + 1):
        progress_bar.progress(i/100)
        time.sleep(0.005)
    
    # Display score
    st.markdown(f'<h4 style="color:{color}">Score: {score}/100</h4>', unsafe_allow_html=True)
    
    # Display feedback
    if feedback:
        st.markdown('<h3>Recommendations to improve your password:</h3>', unsafe_allow_html=True)
        for item in feedback:
            st.markdown(f'<div class="feedback-item">{item}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="feedback-item feedback-success">✅ Your password meets all the recommended criteria!</div>', unsafe_allow_html=True)
    
    # Additional security tips
    with st.expander("Password Security Tips"):
        st.markdown("""
        - Use a unique password for each account
        - Consider using a password manager
        - Enable two-factor authentication when available
        - Avoid using personal information in your passwords
        - Change your passwords periodically
        - Avoid using leaked passwords that are known by malicious actors [^1]
        """)

st.markdown('</div>', unsafe_allow_html=True)

# Password Generator Section
st.markdown('<div class="css-card">', unsafe_allow_html=True)
st.markdown('<h2>🔑 Generate Password</h2>', unsafe_allow_html=True)

# Password generation options
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<p style="font-weight:600; margin-bottom:10px;">Password Length</p>', unsafe_allow_html=True)
    password_length = st.slider("", min_value=8, max_value=32, value=16, step=1, key="length_slider")

with col2:
    st.markdown('<p style="font-weight:600; margin-bottom:10px;">Character Types</p>', unsafe_allow_html=True)
    use_uppercase = st.checkbox("Uppercase (A-Z)", value=True)
    use_lowercase = st.checkbox("Lowercase (a-z)", value=True)
    use_digits = st.checkbox("Numbers (0-9)", value=True)
    use_special = st.checkbox("Special (!@#$%)", value=True)

# Button for generating password
if st.button("Generate Password", key="generate-btn", help="Generate a secure password"):
    generated_password = generate_password(
        password_length, 
        use_uppercase, 
        use_lowercase, 
        use_digits, 
        use_special
    )
    
    # Store in session state
    st.session_state.generated_password = generated_password
    
    # Display the generated password
    st.markdown('<h3 style="margin-top:20px;">Your Generated Password:</h3>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="css-password-display">{generated_password}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)