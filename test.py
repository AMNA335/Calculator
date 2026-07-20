"""
Scientific Calculator - Streamlit App
Controllable via:
  - Keyboard: type directly into the input box, press Enter to evaluate
  - Mouse: click the on-screen calculator buttons
Run with:
    streamlit run scientific_calculator.py
"""

import math
import streamlit as st

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# ----------------------------- Session State ----------------------------- #
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------- Safe Evaluation ---------------------------- #
# Only expose a limited set of safe names to eval()
SAFE_NAMES = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "abs": abs,
    "factorial": math.factorial,
    "pow": pow,
    "pi": math.pi,
    "e": math.e,
    "round": round,
}


def evaluate_expression(expr: str) -> str:
    """Safely evaluate a math expression string and return the result as a string."""
    if not expr.strip():
        return ""
    try:
        # Replace common calculator notation with Python-compatible syntax
        clean_expr = (
            expr.replace("^", "**")
            .replace("×", "*")
            .replace("÷", "/")
            .replace("%", "/100")
        )
        result = eval(clean_expr, {"__builtins__": {}}, SAFE_NAMES)
        result_str = str(result)
        st.session_state.history.insert(0, f"{expr} = {result_str}")
        st.session_state.history = st.session_state.history[:10]
        return result_str
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return "Error: Invalid expression"


# ----------------------------- Callbacks ----------------------------- #
def on_input_change():
    """Triggered when the user types and presses Enter in the text box."""
    expr = st.session_state.expr_box
    st.session_state.expression = expr
    st.session_state.result = evaluate_expression(expr)


def press(value: str):
    """Append a value to the expression when a button is clicked."""
    st.session_state.expression += value
    st.session_state.expr_box = st.session_state.expression


def clear_all():
    st.session_state.expression = ""
    st.session_state.result = ""
    st.session_state.expr_box = ""


def delete_last():
    st.session_state.expression = st.session_state.expression[:-1]
    st.session_state.expr_box = st.session_state.expression


def calculate():
    expr = st.session_state.expression
    st.session_state.result = evaluate_expression(expr)


# ----------------------------- UI ----------------------------- #
st.title("🧮  Welcome Scientific Calculator by Amna")
st.caption("Type using your keyboard and press **Enter**, or click the buttons below.")

st.text_input(
    "Expression",
    key="expr_box",
    value=st.session_state.expression,
    on_change=on_input_change,
    label_visibility="collapsed",
)

if st.session_state.result != "":
    st.markdown(f"### = {st.session_state.result}")

st.write("")  # spacing

# Button layout: (label, value_to_insert)
button_rows = [
    ["sin(", "cos(", "tan(", "π", "e"],
    ["asin(", "acos(", "atan(", "log(", "ln("],
    ["(", ")", "sqrt(", "^", "%"],
    ["7", "8", "9", "/", "AC"],
    ["4", "5", "6", "*", "DEL"],
    ["1", "2", "3", "-", "!"],
    ["0", ".", "=", "+", "exp("],
]

for row in button_rows:
    cols = st.columns(len(row))
    for col, label in zip(cols, row):
        with col:
            if label == "AC":
                st.button(label, on_click=clear_all, use_container_width=True)
            elif label == "DEL":
                st.button(label, on_click=delete_last, use_container_width=True)
            elif label == "=":
                st.button(label, on_click=calculate, use_container_width=True, type="primary")
            elif label == "π":
                st.button(label, on_click=press, args=("pi",), use_container_width=True)
            elif label == "!":
                st.button(label, on_click=press, args=("factorial(",), use_container_width=True)
            else:
                st.button(label, on_click=press, args=(label,), use_container_width=True)

# ----------------------------- History ----------------------------- #
with st.expander("History"):
    if st.session_state.history:
        for item in st.session_state.history:
            st.write(item)
    else:
        st.write("No calculations yet.")

st.divider()
st.caption(
    "Tip: Functions like sin, cos, tan expect degrees. "
    "Use ! for factorial, ^ for power, and % for percent (divides by 100)."
)