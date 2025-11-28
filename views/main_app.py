# --- Importações Essenciais ---
import streamlit as st
import pandas as pd
import cv2
import os
from pathlib import Path

# Módulos Locais
import settings
import helper

def main_app():
    """A aplicação principal de Análise de Materiais Recicláveis."""

    # --- Barra Lateral (Sidebar) ---
    with st.sidebar:
        st.header(f"Bem-vindo, {st.session_state.get('user_name', 'Usuário')}!")

        logo_path = Path(settings.ASSETS_DIR) / "img" / "LOGO.png"
        if logo_path.exists():
            st.image(str(logo_path), width=200)

        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            if "GOOGLE_API_KEY" in os.environ:
                del os.environ["GOOGLE_API_KEY"]
            st.rerun()
        
        st.divider()
        st.header("Configuração da Análise")
        confidence = float(st.slider("Ajuste a Confiança do Modelo", 25, 100, 40)) / 100
        
        st.divider()
        st.header("Configuração da Área de Contagem (ROI)")
        st.markdown("Ajuste a posição e altura da área retangular para contagem de itens.")
        
        roi_center_y_percent = st.slider("Posição Vertical Central da Área (%)", 10, 90, 50, help="Define o centro da faixa de contagem.")
        roi_height_percent = st.slider("Altura da Área (%)", 5, 80, 20, help="Define a espessura da faixa de contagem.")

        st.divider()
        st.header("Configuração da Linha de Contagem")
        st.markdown("Um item será contado ao cruzar a linha **dentro da área verde** na direção escolhida.")
        
        counting_direction = st.selectbox("Direção da Contagem", 
                                          ("De baixo para cima", "De cima para baixo", 
                                           "Da esquerda para a direita", "Da direita para a esquerda"))
        
        line_position_percent = st.slider("Posição da Linha de Contagem (%)", 0, 100, 50, 
                                          help="Posição da linha dentro da área. 0% é o topo/esquerda, 100% é a base/direita.")

        # Definir limites horizontais fixos
        roi_x_start_fixed = 10
        roi_x_end_fixed = 90

        # Calcular Y_start e Y_end a partir do centro e altura
        half_height = roi_height_percent / 2
        roi_y_start_calculated = max(0, int(roi_center_y_percent - half_height))
        roi_y_end_calculated = min(100, int(roi_center_y_percent + half_height))
        
        roi_coords_to_pass = (roi_x_start_fixed, roi_y_start_calculated, roi_x_end_fixed, roi_y_end_calculated)
    
    # --- Interface Principal ---
    st.title("Ucí AI - Análise de Materiais Recicláveis")
    st.markdown("Use a interface abaixo para identificar materiais recicláveis em imagens e vídeos ou para ver o desempenho do modelo de IA.")

    # Carrega o modelo de detecção
    model = helper.load_model(settings.DETECTION_MODEL)
    if not model:
        st.error("O modelo de detecção não pôde ser carregado. Verifique o caminho e as dependências.")
        # Não retorna aqui para permitir que a aba de desempenho seja exibida

    detections_data = []

    st.markdown("""
    <style>
        .st-emotion-cache-1s4xmn4 {
            border: 1px solid #e0e0e0;
            border-radius: 0.5rem;
            padding: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Abas para cada tipo de fonte e para o desempenho
    tab_image, tab_video, tab_webcam, tab_youtube, tab_performance = st.tabs([
        "Análise de Imagens", "Análise de Vídeos", 
        "Análise via Webcam", "Análise do YouTube",
        "Desempenho do Modelo"
    ])

    # --- Aba de Análise de Imagens ---
    with tab_image:
        if not model:
            st.error("Modelo não carregado. Não é possível fazer a análise.")
        else:
            st.subheader("Carregar Imagens para Análise")
            source_imgs = st.file_uploader(
                "Escolha uma ou mais imagens...", 
                type=("jpg", "jpeg", "png", 'bmp', 'webp'), 
                accept_multiple_files=True, 
                label_visibility="collapsed",
                key="image_uploader"
            )
            if st.button('Analisar Imagens', key='analisar_img', type="primary"):
                if source_imgs:
                    with st.spinner("Analisando..."):
                        detections_data, display_images = helper.process_uploaded_images(source_imgs, model, confidence)
                    st.subheader("Resultados da Análise")
                    for item in display_images:
                        col1, col2 = st.columns(2)
                        with col1: st.image(item['original'], caption='Original', use_container_width=True)
                        with col2: st.image(item['detected'], caption='Detectado', use_container_width=True)
                        st.markdown("---")
                else:
                    st.warning("Por favor, carregue ao menos uma imagem para análise.")

    # --- Aba de Análise de Vídeos ---
    with tab_video:
        if not model:
            st.error("Modelo não carregado. Não é possível fazer a análise.")
        else:
            st.subheader("Escolha a Fonte do Vídeo")
            # Removido 'Selecionar da Lista', mantendo apenas 'Fazer Upload de Arquivos'
            # video_source_option = st.radio("Origem:", ["Selecionar da Lista", "Fazer Upload de Arquivos"], horizontal=True, label_visibility="collapsed", key="video_source")
            
            # A funcionalidade de upload de arquivos agora é a única opção
            uploaded_videos = st.file_uploader("Escolha um ou mais arquivos de vídeo...", type=["mp4", "mov", "avi", "mkv"], accept_multiple_files=True, label_visibility="collapsed", key="video_uploader")
            if st.button('Analisar Lote de Vídeos', key='analisar_lote_vid', type="primary"):
                if uploaded_videos:
                    progress_bar = st.progress(0, text="Iniciando análise...")
                    status_text = st.empty()
                    detections_data = helper.process_batch_videos(uploaded_videos, model, confidence, progress_bar, status_text)
                else:
                    st.warning("Por favor, carregue ao menos um vídeo para análise.")
    
    # --- Aba de Análise via Webcam ---
    with tab_webcam:
        if not model:
            st.error("Modelo não carregado. Não é possível fazer a análise.")
        else:
            st.subheader("Análise em Tempo Real com Contagem")
            st.session_state.setdefault('webcam_running', False)
            st.session_state.setdefault('webcam_detections_data', [])
            st.session_state.setdefault('counted_ids', set())
            st.session_state.setdefault('track_history', {})

            col1, col2 = st.columns(2)
            if col1.button("Iniciar Análise", type="primary", key='start_webcam'):
                st.session_state.webcam_running = True
                st.session_state.webcam_detections_data = []
                st.session_state.counted_ids = set()  # Limpa a contagem anterior
                st.session_state.track_history = {} # Limpa o histórico de rastreamento
                st.rerun()
            if col2.button("Parar Análise", key='stop_webcam'):
                st.session_state.webcam_running = False
                st.rerun()

            if st.session_state.webcam_running:
                st.info("Análise da webcam em andamento... Itens serão contados ao passar pela 'Área de Contagem'.")
                vid_cap = cv2.VideoCapture(settings.WEBCAM_PATH)
                col_vid1, col_vid2 = st.columns(2)
                st_frame1 = col_vid1.empty()
                st_frame2 = col_vid2.empty()
                
                while st.session_state.webcam_running:
                    success, image = vid_cap.read()
                    if not success:
                        st.error("Falha ao acessar a webcam.")
                        st.session_state.webcam_running = False
                        break
                    
                    image_resized = cv2.resize(image, (720, int(720 * (9/16))))
                    
                    # Chama a nova função com rastreamento e contagem
                    detected_frame, detected_classes, updated_ids, updated_history = helper.process_video_frame(
                        image_resized, model, confidence, 
                        st.session_state.counted_ids,
                        roi_coords_to_pass,
                        st.session_state.track_history,
                        counting_direction,
                        line_position_percent
                    )
                    
                    # Atualiza os dados de detecção, IDs contados e histórico
                    st.session_state.webcam_detections_data.extend(detected_classes)
                    st.session_state.counted_ids = updated_ids
                    st.session_state.track_history = updated_history
                    
                    st_frame1.image(image_resized, caption='Original', channels="BGR", use_container_width=True)
                    st_frame2.image(detected_frame, caption='Detectado e Contado', channels="BGR", use_container_width=True)
                
                vid_cap.release()
                st.rerun()

            if not st.session_state.webcam_running and st.session_state.webcam_detections_data:
                all_classes = st.session_state.webcam_detections_data
                detected_class_names = [helper.CLASSES.get(cls, "") for cls in sorted(list(set(all_classes)))]
                
                # Calcula a pontuação com base nas classes detectadas
                score = sum(helper.PONTOS_POR_CLASSE.get(helper.CLASSES.get(cls, ""), 0) for cls in all_classes)
                status = "Reciclável" if detected_class_names else "Nenhum item"

                detections_data.append({
                    'Fonte': 'Webcam (Sessão)',
                    'Itens': len(st.session_state.counted_ids), # Usar o total de IDs únicos contados
                    'Classes': detected_class_names,
                    'Pontos': score,
                    'Status': status
                })
                # Limpa os dados para a próxima sessão
                st.session_state.webcam_detections_data = []
                st.session_state.counted_ids = set()

    # --- Aba de Análise do YouTube ---
    with tab_youtube:
        if not model:
            st.error("Modelo não carregado. Não é possível fazer a análise.")
        else:
            st.subheader("Análise de Vídeo do YouTube")
            source_youtube = st.text_input("Cole a URL do vídeo do YouTube aqui:")
            
            if st.button("Analisar Vídeo do YouTube", type="primary", key='start_youtube'):
                if source_youtube:
                    with st.spinner("Analisando vídeo do YouTube..."):
                        stream_url = helper.get_youtube_stream_url(source_youtube)
                        if stream_url:
                            vid_cap = cv2.VideoCapture(stream_url)
                            detections_data = helper.process_video_stream(vid_cap, model, confidence, source_name=source_youtube)
                        else:
                            st.error("Não foi possível processar a URL do YouTube.")
                else:
                    st.warning("Por favor, insira uma URL do YouTube.")

    # --- Aba de Desempenho do Modelo ---
    with tab_performance:
        st.header("Desempenho e Métricas do Modelo YOLO")
        st.markdown("Esta página apresenta os resultados quantitativos obtidos durante a fase de treinamento e validação do modelo de detecção.")
        st.markdown("---")
        st.subheader("Resumo das Métricas de Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("mAP@0.5 (Mean Avg. Precision)", "90.7%")
        col2.metric("Precisão (Precision)", "88.3%")
        col3.metric("Recall (Revocação)", "85.3%")
        with st.expander("🔍 O que essas métricas significam?"):
            st.markdown("""
            - **mAP (Mean Average Precision):** É a principal métrica para modelos de detecção de objetos. Ela combina Precisão e Recall em uma única métrica que avalia a performance geral do modelo em todas as classes.
            - **Precisão (Precision):** De todas as detecções que o modelo fez, quantas estavam corretas? Uma alta precisão significa poucas detecções falsas.
            - **Recall (Revocação):** De todos os objetos que realmente existiam nas imagens, quantos o modelo conseguiu encontrar? Um alto recall significa que o modelo deixou poucos objetos passarem despercebidos.
            """
        )
        st.markdown("---")
        st.subheader("Visualização dos Resultados do Treinamento")
        results_graph_path = settings.TRAINING_RESULTS_DIR / "results.png"
        confusion_matrix_path = settings.TRAINING_RESULTS_DIR / "confusion_matrix.png"
        pr_curve_path = settings.TRAINING_RESULTS_DIR / "PR_curve.png"
        if results_graph_path.exists():
            st.markdown("#### Curvas de Aprendizagem")
            st.image(str(results_graph_path), caption="Evolução das métricas ao longo das épocas de treinamento.")
        else:
            st.warning(f"Imagem 'results.png' não encontrada em '{results_graph_path}'.")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            if confusion_matrix_path.exists():
                st.markdown("#### Matriz de Confusão")
                st.image(str(confusion_matrix_path), caption="Acertos e erros de classificação do modelo entre as classes.")
            else:
                st.warning(f"Imagem 'confusion_matrix.png' não encontrada em '{confusion_matrix_path}'.")
        with col_img2:
            if pr_curve_path.exists():
                st.markdown("#### Curva de Precisão-Recall")
                st.image(str(pr_curve_path), caption="Trade-off entre Precisão e Recall.")
            else:
                st.warning(f"Imagem 'PR_curve.png' não encontrada em '{pr_curve_path}'.")

    # --- Seção de Relatório Final (Fora das abas) ---
    if detections_data:
        st.markdown("---")
        st.header("Relatório Final da Análise")
        st.subheader("Estatísticas Consolidadas")
        
        report_df = pd.DataFrame(detections_data)
        st.dataframe(report_df)

        # Calcular pontuação total e gerar cupom
        total_score = report_df['Pontos'].sum()

        if total_score > 0:
            st.subheader("🎉 Cupom de Desconto Gerado! 🎉")
            credit_value = total_score * 0.01  # 1 ponto = R$ 0,01
            coupon_code = helper.generate_coupon_code()
            
            col1, col2 = st.columns(2)
            col1.metric("Pontuação Total", f"{total_score} pts")
            col2.metric("Valor do Crédito", f"R$ {credit_value:.2f}")
            
            st.success(f"**Use o código abaixo para seu desconto:**")
            st.code(coupon_code, language=None)

        with st.spinner("Gerando gráficos e PDF..."):
            graph_images = helper.create_graphs_in_memory(detections_data)
            if graph_images:
                st.subheader("Análise Gráfica")
                num_cols = min(len(graph_images), 3)
                cols = st.columns(num_cols)
                col_index = 0
                for title, path in graph_images.items():
                    if Path(path).exists():
                        with cols[col_index]:
                            st.image(path, caption=title.replace('_', ' ').title(), use_container_width=True)
                        col_index = (col_index + 1) % num_cols
            
            st.subheader("Download do Relatório Completo (com Cupom)")
            pdf_file_path = helper.generate_pdf_report(detections_data, graph_images)
            with open(pdf_file_path, "rb") as f:
                st.download_button("Baixar Relatório em PDF", f, file_name="relatorio_analise_uci_ai.pdf", type="primary")