import streamlit as st
import requests
import json
from pathlib import Path
from datetime import datetime
from io import BytesIO
import os

st.set_page_config(page_title="SOC Agent (n8n) UI", layout="wide")

HISTORY_FILE = Path(__file__).parent / 'soc_history.json'
HISTORY_DIR = Path(__file__).parent / 'soc_reports'
HISTORY_DIR.mkdir(exist_ok=True)


def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return []
    return []


def save_history(history):
    try:
        HISTORY_FILE.write_text(json.dumps(
            history, ensure_ascii=False, indent=2))
    except Exception:
        pass


def generate_pdf_bytes(title: str, target: str, result_text: str, timestamp: str) -> bytes:
    try:
        from fpdf import FPDF
    except Exception:
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font('Arial', size=12)
    pdf.ln(4)
    pdf.cell(0, 8, f'Target: {target}', ln=True)
    pdf.cell(0, 8, f'Date: {timestamp}', ln=True)
    pdf.ln(6)
    # split text into lines
    for line in result_text.split('\n'):
        pdf.multi_cell(0, 6, line)

    bio = BytesIO()
    pdf.output(bio)
    return bio.getvalue()


def main():
    st.title('SOC Agent — n8n (Webhook)')

    # Sidebar: webhook config and history
    st.sidebar.header('Configuração')
    default_webhook = os.environ.get('N8N_SOC_WEBHOOK', '')
    webhook_url = st.sidebar.text_input(
        'Webhook URL (n8n)', value=st.session_state.get('n8n_webhook', default_webhook))
    st.session_state['n8n_webhook'] = webhook_url

    history = load_history()
    st.sidebar.markdown('**Histórico de investigações**')
    if history:
        for i, h in enumerate(history[:20]):
            label = f"{h['timestamp'][:19]} — {h['target'][:40]}"
            if st.sidebar.button(label, key=f'hist_{i}'):
                st.session_state['selected'] = h
    else:
        st.sidebar.write('Nenhuma investigação ainda')

    st.sidebar.markdown('---')
    if st.sidebar.button('Limpar histórico'):
        history = []
        save_history(history)
        st.experimental_rerun()

    # Main input
    st.subheader('Nova investigação')
    col1, col2 = st.columns([3, 1])
    with col1:
        target = st.text_input('IP ou URL para investigar', '')
        notes = st.text_area('Notas (opcional)', height=80)
    with col2:
        st.write('Tipo')
        t = st.selectbox('Selecione', ['auto', 'ip', 'url'])
        send = st.button('Enviar para agente SOC')

    if send:
        if not webhook_url:
            st.error('Insira a URL do webhook na sidebar antes de enviar.')
        elif not target.strip():
            st.error('Insira um IP ou URL válido.')
        else:
            payload = {
                'target': target.strip(),
                'type': t,
                'notes': notes,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            try:
                with st.spinner('Enviando para o agente...'):
                    resp = requests.post(webhook_url, json=payload, timeout=30)
                try:
                    result = resp.json()
                    pretty = json.dumps(result, ensure_ascii=False, indent=2)
                except Exception:
                    pretty = resp.text

                st.subheader('Resultado da investigação')
                st.code(pretty, language='json')

                entry = {
                    'target': target,
                    'notes': notes,
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'response': result if isinstance(result, dict) else {'text': pretty}
                }
                history.insert(0, entry)
                save_history(history)
                st.success('Resultado salvo no histórico.')

                # offer PDF export
                timestamp = entry['timestamp']
                title = 'SOC Investigation Report'
                result_text = pretty
                pdf_bytes = generate_pdf_bytes(
                    title, target, result_text, timestamp)
                if pdf_bytes:
                    fname = f"soc_report_{target.replace('://', '_').replace('/', '_')}_{timestamp[:19].replace(':', '-')}.pdf"
                    st.download_button(
                        'Exportar resultado em PDF', data=pdf_bytes, file_name=fname, mime='application/pdf')
                else:
                    # fallback: download JSON
                    st.download_button('Exportar resultado (JSON)', data=json.dumps(entry, ensure_ascii=False, indent=2).encode(
                        'utf-8'), file_name='soc_result.json', mime='application/json')

            except requests.RequestException as e:
                st.error(f'Erro de rede ao chamar o webhook: {e}')

    # If selected history item
    if 'selected' in st.session_state:
        h = st.session_state['selected']
        st.subheader('Investigação selecionada')
        st.markdown(f"**Target:** {h['target']}")
        st.markdown(f"**Data:** {h['timestamp']}")
        if h.get('notes'):
            st.markdown(f"**Notas:** {h['notes']}")
        st.markdown('**Resposta:**')
        st.json(h.get('response', {}))
        # allow export
        pdf_bytes = generate_pdf_bytes('SOC Investigation Report', h['target'], json.dumps(
            h.get('response', {}), ensure_ascii=False, indent=2), h['timestamp'])
        if pdf_bytes:
            fname = f"soc_report_{h['target'].replace('://', '_').replace('/', '_')}_{h['timestamp'][:19].replace(':', '-')}.pdf"
            st.download_button('Exportar como PDF', data=pdf_bytes,
                               file_name=fname, mime='application/pdf')
        else:
            st.download_button('Exportar (JSON)', data=json.dumps(h, ensure_ascii=False, indent=2).encode(
                'utf-8'), file_name='soc_history_item.json', mime='application/json')


if __name__ == '__main__':
    main()
