# DataBot AI - Akıllı Veri Analiz Asistanı 🤖

DataBot, yerel bir dil modeli (Llama 3.1) kullanarak Excel dosyalarındaki verileri analiz eden ve harici API'lerden (örn. Hava Durumu) canlı bilgi çekebilen gelişmiş bir **AI Agent** projesidir.

## Mimari Özet:

Bu proje, modelin sadece kendi bilgisini kullanmak yerine dış kaynaklara (Excel ve API) başvurmasını sağlayan Function Calling (Fonksiyon Çağırma) yapısını kullanır. Elde edilen bu veriler RAG (Veri Artırımlı Üretim) yaklaşımıyla modele "bağlam" olarak sunulur; böylece model bilgi uydurmak (halüsinasyon) yerine yalnızca doğrulanmış gerçek verilerle cevap üretmeye zorlanır.

## 📂 Proje Klasör Yapısı
* `app.py`: Streamlit tabanlı modern web arayüzü.
* `agent.py`: Karar verici ajan (Orchestration) ve RAG mantığı.
* `tools.py`: Veri erişim katmanı (Excel okuma & harici API).
* `data/`: Excel (`.xlsx`) formatındaki veri setlerini içeren klasör.
* `requirements.txt`: Proje bağımlılıkları.

---

## ⚙️ Kurulum ve Çalıştırma Talimatları

Projeyi kendi bilgisayarınızda izole bir ortamda çalıştırmak için aşağıdaki adımları sırasıyla izleyin.

### Adım 1: Sanal Ortam (Virtual Environment) Kurulumu
Proje dizininde bir terminal açın ve sanal ortam oluşturun:

```bash
python -m venv venv
```

Sanal ortamı aktif hale getirin:

* **Windows için:** `venv\Scripts\activate`
* **Mac/Linux için:** `source venv/bin/activate`

### Adım 2: Gerekli Kütüphanelerin Yüklenmesi
Sanal ortam aktifken (terminal satırının başında `(venv)` yazmalıdır), proje bağımlılıklarını yükleyin:

```bash
pip install -r requirements.txt
```

### Adım 3: Lokal LLM (Llama 3.1) Bağlantısının Kurulması
Bu proje, veri gizliliğini sağlamak adına bulut tabanlı API'ler yerine **Ollama** üzerinden lokal Llama 3.1 modelini kullanır. Bu nedenle harici bir API Key (OpenAI vb.) gerektirmez. Sistemdeki `api_key='ollama'` parametresi lokal sunucu için kullanılan sembolik bir anahtardır.

1. Bilgisayarınızda [Ollama] (https://ollama.com/) yüklü değilse kurun.
2. Terminalden Llama 3.1 modelini indirin ve başlatın:

```bash
ollama run llama3.1
```
*(Model arka planda çalışmaya devam edecektir, bu terminali açık bırakabilir veya `Ctrl+D` tuş kombinasyonu ile arka plana atabilirsiniz).*

### Adım 4: Web Arayüzünü Başlatma
Farklı bir terminal açın (sanal ortamın aktif olduğundan emin olun) ve DataBot arayüzünü çalıştırın:

```bash
python -m streamlit run app.py
```
Tarayıcınızda açılan ekranda örnek soruları tıklayarak veya kendi sorularınızı yazarak asistanı test edebilirsiniz.

---

## 💡 Test Senaryoları (Örnek Sorular)
* "En az yakıt tüketen araç hangisi?" *(Statik Excel verisi testi)*
* "Önümüzdeki hafta İstanbul'da hava nasıl olacak?" *(Canlı API testi)*
* "Resmi tatiller nelerdir?" *(Eksik veya farklı veri kaynağı testi)*

<img width="1640" height="888" alt="image" src="https://github.com/user-attachments/assets/1a8e5904-399f-4931-8ce5-fcfe55b0b831" />
