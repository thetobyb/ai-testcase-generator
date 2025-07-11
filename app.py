# app.py
import streamlit as st
from generator import generate_test_cases
import hashlib
import pandas as pd

st.set_page_config(page_title="AI Test Case Generator", layout="centered")
st.markdown(
    """
    <div style="position: relative; left: -80px;">
        <h1 style='white-space: nowrap;'>
        🧪 AI AC and Test Case Generator
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

def is_product_owner_mode():
    return test_depth == "Product-Owner"

# -- Helper: Detect input type --
def detect_input_type(text: str) -> str:
    if text.strip().startswith("mutation") or text.strip().startswith("query") or "{" in text:
        return "graphql"
    elif "As a user" in text or "Given" in text:
        return "story"
    else:
        return "unknown"

# -- Test depth selector --
test_depth = st.selectbox("Select test depth", ["Simple", "Detailed", "Edge-heavy", "Product-Owner"])

# -- Input --
user_input = st.text_area("Paste a user story, ticket description or GraphQL mutation", height=200)

# -- Generate button --
if st.button("🚀 Generate Test Cases"):
    if user_input.strip():
        with st.spinner("Generating test cases..."):
            input_type = detect_input_type(user_input)

            # Customize prompt slightly
            if input_type == "graphql":
                context = "This is a GraphQL mutation or query. Generate test cases for API validation, edge cases, and response handling."
            elif input_type == "story":
                context = "This is a user story or requirement. Generate relevant functional test cases."
            else: 
                context = "This is a user story description. Generate acceptance criteria in the BDD format using Given, When, Then"

            if test_depth == "Detailed":
                context += " Include validations, boundary values, and some exploratory cases."
            elif test_depth == "Edge-heavy":
                context += " Focus on rare edge cases, invalid data, and unexpected inputs."
            elif test_depth == "Product-Owner":
                context = "This is a user story description. Generate acceptance criteria in the BDD format using Given, When, Then"

            output = generate_test_cases(user_input, context)

            # Display results
            if is_product_owner_mode():
                st.markdown("### 📋 Generated Acceptance Criteria")
            else:
                st.markdown("### ✅ Generated Test Cases")

            items = [case.strip() for case in output.split("\n\n") if case.strip()]

            for i, item in enumerate(items, start=1):
                title = f"Acceptance Criteria {i}" if is_product_owner_mode() else f"Test Case {i}"
                with st.expander(title):
                    if is_product_owner_mode():
                        lines = item.split("\n")
                        for line in lines:
                            line = line.strip()
                            if line:
                                st.markdown(f"- {line}")
                    else:
                        st.markdown(item)

            # CSV export block (inside the button scope!)
            if len(items) > 1:
                col_name = "Acceptance Criteria" if is_product_owner_mode() else "Test Case"
                df = pd.DataFrame([{col_name: c} for c in items])
                csv = df.to_csv(index=False)
                st.download_button("⬇️ Download as CSV", csv, file_name="results.csv", mime="text/csv")
    else:
        st.warning("Please enter a user story or GraphQL mutation.")
