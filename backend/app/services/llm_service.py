import google.generativeai as genai
from ..config import settings
import json
from typing import Dict, Any

genai.configure(api_key=settings.gemini_api_key)

class LLMService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def parse_transaction(self, user_message: str) -> Dict[str, Any]:
        prompt = f"""
Kamu adalah asisten akunting untuk UMKM. Analisis pesan berikut dan ekstrak informasi transaksi.

Pesan: "{user_message}"

Identifikasi:
1. Tipe transaksi (income/expense/receivable/payable)
2. Jumlah uang (dalam angka)
3. Kategori (contoh: penjualan, gaji, operasional, hutang, piutang)
4. Deskripsi singkat

Berikan response dalam format JSON:
{{
    "transaction_type": "income|expense|receivable|payable",
    "amount": 0,
    "category": "kategori",
    "description": "deskripsi"
}}

Jika tidak bisa diparse, return {{"error": "Tidak dapat memahami transaksi"}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            result = json.loads(text)
            return result
        except Exception as e:
            return {"error": f"Error parsing: {str(e)}"}
    
    def answer_accounting_question(self, question: str, context: str = "") -> str:
        prompt = f"""
Kamu adalah asisten akunting untuk UMKM Indonesia. Jawab pertanyaan berikut dengan jelas dan praktis.

Konteks: {context if context else "Tidak ada konteks khusus"}

Pertanyaan: {question}

Berikan jawaban yang mudah dipahami oleh pemilik UMKM.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Maaf, terjadi error: {str(e)}"
    
    def generate_summary(self, transactions_data: Dict[str, Any]) -> str:
        prompt = f"""
Buatkan ringkasan keuangan dalam bahasa Indonesia yang mudah dipahami berdasarkan data berikut:

{json.dumps(transactions_data, indent=2)}

Format ringkasan:
- Total pemasukan
- Total pengeluaran
- Saldo
- Kategori pengeluaran terbesar
- Insight dan rekomendasi singkat
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Maaf, tidak dapat membuat ringkasan: {str(e)}"

llm_service = LLMService()
