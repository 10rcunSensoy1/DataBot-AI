import streamlit as st
from agent import run_agent

# Sayfa Konfigürasyonu
st.set_page_config(page_title="DataBot AI", page_icon="🤖", layout="centered")

st.title("🤖 DataBot AI")
st.markdown("Verileriniz hakkında soru sorun, DataBot analiz etsin.")

# Sohbet geçmişini tutma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ÖRNEK SORULAR (TIKLANABİLİR BUTONLAR) ---
st.markdown("### 💡 Örnek Sorular")
col1, col2, col3 = st.columns(3)

# Kullanıcının butona tıklaması durumunda soruyu yakalamak için boş bir değişken
secilen_soru = None

if col1.button("🚗 En az yakan araç hangisi?"):
    secilen_soru = "Hangi araç daha az yakıt tüketiyor?"
if col2.button("⛅ Haftaya hava nasıl?"):
    secilen_soru = "Önümüzdeki hafta İstanbul'da hava nasıl olacak?"
if col3.button("📅 Tatiller ne zaman?"):
    secilen_soru = "Resmi tatiller hangi günlere denk geliyor?"

# --- SOHBET GİRDİSİ (INPUT) ---
# Kullanıcı ya mesaj yazmıştır ya da yukarıdaki butonlardan birine tıklamıştır
prompt = st.chat_input("Sorunuzu buraya yazın...") or secilen_soru

if prompt:
    # 1. Kullanıcının sorusunu ekrana bas ve geçmişe kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Asistanın düşünme ve cevap verme aşaması
    with st.chat_message("assistant"):
        with st.spinner("DataBot verileri tarıyor..."):
            response = run_agent(prompt)
            st.markdown(response)
    
    # 3. Asistanın cevabını geçmişe kaydet
    st.session_state.messages.append({"role": "assistant", "content": response})