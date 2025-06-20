import streamlit as st
import importlib

st.set_page_config(page_title="Презентации по паттернам", layout="wide")
st.title("Презентации по шаблонам проектирования")

# Боковое меню выбора
page = st.sidebar.selectbox("Выберите презентацию", ["Flyweight", "Chain of Responsibility"])

if page == "Flyweight":
    import flyweight
    flyweight.show()
elif page == "Chain of Responsibility":
    import chain_of_responsibility
    chain_of_responsibility.show()
