# --- Importações Essenciais ---
import streamlit as st
import base64
import os

def welcome_screen():
    """Exibe a tela de boas-vindas com um design aprimorado e moderno para a Ucí AI."""

    # CSS para estilizar os cartões e a página
    st.markdown("""
    <style>
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 25px 20px;
        text-align: center;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        transition: 0.3s;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .card h5 {
        color: #495057;
        font-size: 1.2rem;
        margin-bottom: 15px;
        text-align: center;
    }
    .card p {
        color: #6c757d;
        text-align: center;
        font-size: 0.95rem;
    }
    .stButton>button {
        font-size: 1.1rem;
        padding: 10px 24px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Seção Hero ---
    with st.container():
        logo_path = "assets/img/LOGO.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(
                f"<div style='text-align: center; padding-bottom: 20px;'><img src='data:image/png;base64,{data}' width='300'></div>",
                unsafe_allow_html=True
            )
        
        st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Bem-vindo à Ucí AI</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #34495e; margin-bottom: 30px;'>Sua solução inteligente para análise de materiais recicláveis</h3>", unsafe_allow_html=True)

        _ , btn_col, _ = st.columns([2.5, 1.5, 2.5])
        with btn_col:
            if st.button("♻️ Iniciar Análise", use_container_width=True, type="primary"):
                st.session_state.welcome_seen = True
                st.rerun()

    st.markdown("--- ")

    # --- Seção de Funcionalidades ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Funcionalidades Principais</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div style='font-size: 4rem;'>🤖</div>
            <h5>Detecção por IA</h5>
            <p>Utilize nosso modelo de Inteligência Artificial para detectar e classificar automaticamente materiais recicláveis como garrafas e latas em imagens e vídeos.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div style='font-size: 4rem;'>📄</div>
            <h5>Relatórios Completos</h5>
            <p>Receba um relatório detalhado da análise, com a contagem de itens, gráficos e um cupom de desconto baseado nos materiais reciclados.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div style='font-size: 4rem;'>🎥</div>
            <h5>Múltiplas Fontes</h5>
            <p>Analise mídias de diversas fontes, incluindo upload de imagens e vídeos, webcam em tempo real ou links do YouTube.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("--- ")

    # --- Seção ODS ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Contribuindo para um Futuro Sustentável</h2>", unsafe_allow_html=True)
    
    sdg_col1, sdg_col2 = st.columns(2)
    with sdg_col1:
        st.markdown("""
        <div class="card">
            <img src="data:image/png;base64,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" style="width:120px; margin-left:auto; margin-right:auto; margin-bottom:15px;">
            <h5>ODS 11: Cidades e Comunidades Sustentáveis</h5>
            <p>Ao facilitar a identificação e separação de materiais recicláveís, nossa IA contribui diretamente para a melhoria da gestão de resíduos sólidos nas cidades. Isso ajuda a reduzir o volume de lixo em aterros sanitários, diminui a poluição e apoia a criação de infraestruturas urbanas mais limpas e sustentáveis para todos.</p>
        </div>
        """, unsafe_allow_html=True)
    with sdg_col2:
        st.markdown("""
        <div class="card">
            <img src="data:image/jpeg;base64,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" style="width:120px; margin-left:auto; margin-right:auto; margin-bottom:15px;">
            <h5>ODS 12: Consumo e Produção Responsáveis</h5>
            <p>Promovemos ativamente a transição para uma economia circular. Ao transformar resíduos em recursos e recompensar os usuários com créditos, a Ucí AI cria um incentivo claro para o descarte correto e a reciclagem. Capacitamos consumidores e empresas a fazerem escolhas mais responsáveis, fechando o ciclo de produção e minimizando o impacto ambiental.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("--- ")

    # --- Como Começar ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Como Começar</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div style='font-size: 3.5rem; color: #0d6efd; font-weight: 600;'>1️⃣</div>
            <h5 style="margin-top: 15px;">Inicie a Análise</h5>
            <p>Clique no botão 'Iniciar Análise' para acessar a plataforma de detecção.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div style='font-size: 3.5rem; color: #0d6efd; font-weight: 600;'>2️⃣</div>
            <h5 style="margin-top: 15px;">Escolha a Fonte</h5>
            <p>Selecione a aba correspondente à fonte de sua mídia: imagem, vídeo, webcam ou YouTube.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div style='font-size: 3.5rem; color: #0d6efd; font-weight: 600;'>3️⃣</div>
            <h5 style="margin-top: 15px;">Receba seu Cupom</h5>
            <p>Após a análise, visualize o relatório, a pontuação e o cupom de desconto gerado para você.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Seção da Equipe ---
    st.markdown("--- ")
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Nossa Equipe</h2>", unsafe_allow_html=True)

    # CSS para as imagens da equipe
    st.markdown("""
    <style>
    .team-member-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Membros da equipe
    team_members = [
        {"name": "Breno Lucas dos Anjos Silva", "email": "breno.anjossilva1@gmail.com", "image": "assets/img/breno.jpg"},
        {"name": "Caroline Cruz da Silva", "email": "caroline.ufopa@gmail.com", "image": "assets/img/carol.jpg"},
        {"name": "Enzo Gabriel Freitas Conduru de Souza", "email": "enzogabriel.2006.15@gmail.com", "image": "https://fpoimg.com/150x150?text=Member"},
        {"name": "Felipe Rafael dos Santos Barbosa", "email": "rafaelt.ibarbosa@gmail.com", "image": "https://fpoimg.com/150x150?text=Member"},
        {"name": "João Irineu Furtado da Silva Neto", "email": "joaoirineusilvaneto@gmail.com", "image": "https://fpoimg.com/150x150?text=Member"},
        {"name": "João Paulo da Silva Cardoso", "email": "jpscardoso@ufpa.br", "image": "assets/img/jpc.jpg"},
        {"name": "Victor Amazonas Viegas Ferreira", "email": "viegasdeveloper@gmail.com", "image": "https://fpoimg.com/150x150?text=Member"}
    ]

    # Exibir membros da equipe em um grid
    cols = st.columns(3)
    for i, member in enumerate(team_members):
        with cols[i % 3]:
            image_path = member["image"]
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                image_html = f"<img class='team-member-img' src='data:image/png;base64,{data}'>"
            else:
                image_html = f"<img class='team-member-img' src='{image_path}'>"

            st.markdown(f"""
            <div class="card">
                {image_html}
                <h5>{member["name"]}</h5>
                <p>{member["email"]}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- Rodapé ---
    st.markdown("<p style='text-align: center; color: #7f8c8d; padding-top: 30px;'>Uma solução inteligente para um planeta mais limpo.</p>", unsafe_allow_html=True)

