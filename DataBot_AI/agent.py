from datetime import datetime
from openai import OpenAI
import json
import tools 

# 1. Lokal LLM Yapılandırması
# Ollama üzerinden Llama 3.1 modeline standart OpenAI SDK'sı ile erişim sağlanır.
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

# 2. Araç (Tool) Tanımlamaları
# Modelin hangi durumlarda hangi veri kaynağına başvuracağını belirleyen fonksiyon şemaları.
tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_holidays_info",
            "description": "Resmi ve dini tatillerin bilgisini Excel veri setinden döndürür."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_vehicle_info",
            "description": "Araç teknik özelliklerini ve yakıt tüketim verilerini Excel üzerinden döndürür."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_historical_weather_info",
            "description": "İstanbul'un geçmiş yıllara ait istatistiksel hava verilerini döndürür."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather_forecast",
            "description": "Önümüzdeki günlerin güncel hava tahminlerini harici API üzerinden getirir.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Hava durumu istenen şehir."
                    }
                },
                "required": ["city"]
            }
        }
    }
]

def run_agent(user_query: str):
    print(f"\n>>> Kullanıcı Sorusu: {user_query}")
    
    # Zaman Körlüğü Çözümü: Çalıştırıldığı anın güncel tarihini dinamik olarak alır.
    bugun = datetime.now().strftime("%d %B %Y")
    
    messages = [
        {
            "role": "system", 
            "content": f"Sen bir veri analiz asistanısın. Bugünün tarihi: {bugun}. Uygun aracı seçerek kullanıcıyı yanıtlamalısın."
        },
        {"role": "user", "content": user_query}
    ]

    # ADIM 1: Uygun Veri Kaynağının Seçilmesi (Function Selection)
    print("[Sistem]: Soru analiz ediliyor...")
    response = client.chat.completions.create(
        model="llama3.1",
        messages=messages,
        tools=tools_list,
        temperature=0
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # ADIM 2: Dinamik Fonksiyon Çağrısı ve Veri Eldesi
    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name 
            
            print(f"[Sistem]: '{function_name}' veri aracı çalıştırılıyor...")
            function_to_call = getattr(tools, function_name)
            
            # Parametre uyumsuzluklarına karşı hata toleransı (Robustness)
            try:
                if tool_call.function.arguments:
                    function_args = json.loads(tool_call.function.arguments)
                    function_result = function_to_call(**function_args)
                else:
                    function_result = function_to_call()
            except TypeError:
                function_result = function_to_call()
            
            # ADIM 3: RAG (Retrieval-Augmented Generation) Uygulaması
            # Elde edilen ham veri, halüsinasyonu engellemek için izele bir bağlamda sentezlenir.
            # Sistem promptuna geçmiş tarihleri filtreleme kuralı katı bir şekilde eklendi.
            print("[Sistem]: Veri sentezleniyor...")
            final_messages = [
                {
                    "role": "system",
                    "content": (
                        f"Sen bir veri özetleme asistanısın. Bugünün tarihi: {bugun}.\n"
                        "SADECE aşağıda sunulan 'ELDE EDİLEN VERİ' bilgilerini kullanarak cevap üret. "
                        "Veride olmayan hiçbir bilgiyi uydurma.\n\n"
                        "ZAMAN KURALI: Kullanıcı 'önümüzdeki', 'gelecek' veya 'yaklaşan' gibi kelimelerle "
                        f"tatil veya zaman bilgisi istediğinde, bugünün tarihinden ({bugun}) önce gerçekleşmiş "
                        "ve geçmişte kalmış olan tatilleri (Örn: Ocak, Nisan, Mayıs ayları gibi) KESİNLİKLE yanıta dahil etme. "
                        "Yalnızca bugünden sonraki gün ve aylara ait tatilleri listele."
                    )
                },
                {
                    "role": "user",
                    "content": f"SORU: {user_query}\n\nELDE EDİLEN VERİ:\n{function_result}"
                }
            ]

            final_response = client.chat.completions.create(
                model="llama3.1",
                messages=final_messages,
                temperature=0
            )
            print(f"\n[Asistan]: {final_response.choices[0].message.content}")
            return final_response.choices[0].message.content
    
    else:
        print(f"\n[Asistan]: {response_message.content}")
        return response_message.content

if __name__ == "__main__":
    # Test Senaryosu 1: Excel veri çekme
    run_agent("Hangi araç daha az yakıt tüketiyor?")
    print("-" * 30)
    # Test Senaryosu 2: Harici API sorgusu
    run_agent("Önümüzdeki hafta İstanbul'da hava nasıl olacak?")