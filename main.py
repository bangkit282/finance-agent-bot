from flask import Flask, request
import datetime
import requests

app = Flask(__name__)

# Untuk testing sementara, bisa pakai link sheet.best dummy dulu
SHEET_URL = "https://api.sheetbest.com/sheets/015f31b8-16ea-46c0-84a4-7d76c22a6f05"

def parse_message(msg):
    if msg.startswith('+'):
        jenis = 'Pemasukan'
        jumlah, *keterangan = msg[1:].strip().split(' ', 1)
    elif msg.startswith('-'):
        jenis = 'Pengeluaran'
        jumlah, *keterangan = msg[1:].strip().split(' ', 1)
    else:
        return None

    return {
        "Tanggal": datetime.datetime.now().strftime("%d/%m/%Y"),
        "Jenis": jenis,
        "Jumlah": int(jumlah),
        "Keterangan": keterangan[0] if keterangan else ""
    }

@app.route("/")
def home():
    return "✅ Bot Keuangan Aktif"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    msg_body = request.form.get('Body')
    data = parse_message(msg_body)
    if data:
        requests.post(SHEET_URL, json=data)
        return f"{data['Jenis']} sebesar Rp{data['Jumlah']} dicatat."
    return "⚠️ Format salah. Gunakan + atau - di awal pesan."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
