# --- Importações Essenciais ---
import streamlit as st

# Importa as funções de cada página
from views.welcome import welcome_screen
from views.main_app import main_app

# --- CONFIGURAÇÃO DA PÁGINA (DEVE SER O PRIMEIRO COMANDO STREAMLIT) ---
st.set_page_config(
    page_title="Ucí AI",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Bloco de Execução Principal (Roteador) ---

# Inicializa o estado da sessão se não existir
if "welcome_seen" not in st.session_state:
    st.session_state.welcome_seen = False

# Controla qual página é exibida
if not st.session_state.welcome_seen:
    welcome_screen()
else:
    main_app()
