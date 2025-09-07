import random
from flask import Flask, render_template, request, jsonify, session
import re

app = Flask(__name__)
app.secret_key = 'kunci-rahasia-game-pacaran-regex'

GAME_OVER_MESSAGES = [
    "Emang kamu gapernah ngertiin aku. Semua ini kayak game aja buat kamu. Kita PUTUSS! 🤬",
    "Kamu sayang ga sih sama aku? Disuruh ngertiin regex doang kok susah bgt… KITA PUTUS AJA!!"
]

WIN_MESSAGE = "SELAMAT! Kamu berhasil mencapai akhir cerita.<br><br>Kamu telah belajar bahasa cinta yang paling unik: Regex. Setiap pola yang kamu tebak bukan hanya barisan kode, tapi juga bukti kesabaran dan pengertianmu.<br><br>Hubunganmu kini lebih kuat dari sebelumnya. Kalian berhasil! 💖"

GAME_LEVELS = [
    # === DAY 1 ===
    {
        "day": 1,
        "opening": "Hai! Selamat datang di permulaan perjalanan cinta regex kmu 😝 Hayo coba tebak apa sih yang sebenernya cewe kamu katakan. Happy decoding!!",
        "question": "Eh sumpah semalem panas bgt deh, tidurku jadi ga nyenyak bgt flop 👎! Aku mau ^[a-z][ae]ndi$ dulu deh yang!",
        "regex": r"^mandi$",
        "success": "Aduhaii aku laper bgt hari ini yang… ^[mn]as[ae]k$ soto enak nih keknya"
    },
    {
        "day": 1,
        "question": "Aduhaii aku laper bgt hari ini yang… ^[mn]as[ae]k$ soto enak nih keknya",
        "regex": r"^masak$",
        "success": "Yey kenyang! Duh ini kalau based on kontrak kuliah aku besok quiz, tapi ngantuk bgt, tidur dulu deh baru ^[bp]elaj[ae]r$"
    },
    {
        "day": 1,
        "question": "Yey kenyang! Duh ini kalau based on kontrak kuliah aku besok quiz, tapi ngantuk bgt, tidur dulu deh baru ^[bp]elaj[ae]r$",
        "regex": r"^belajar$",
        "success": "Abis belajar waktunya mukbang lagii! Aku mau bikin ^[rst]am[ae][mn]$ , trus nanti mau sambil nonton anime ah! Kamu nonton anime juga dong biar kita chika dance 🥰"
    },
    {
        "day": 1,
        "question": "Abis belajar waktunya mukbang lagii! Aku mau bikin ^[rst]am[ae][mn]$ , trus nanti mau sambil nonton anime ah! Kamu nonton anime juga dong biar kita chika dance 🥰",
        "regex": r"^ramen$",
        "success": "Eh udah sore nihh? Biar body goals, aku mau ^[jy]o[gj]a$ dulu ya beb, ttyl 👋"
    },
    {
        "day": 1,
        "question": "Eh udah sore nihh? Biar body goals, aku mau ^[jy]o[gj]a$ dulu ya beb, ttyl 👋",
        "regex": r"^yoga$",
        "success": "Segernyaa mandi abis yoga! Hmm pake piyama warna biru atau ^ku[nm]i[ng]$ yaaa?"
    },
    {
        "day": 1,
        "question": "Segernyaa mandi abis yoga! Hmm pake piyama warna biru atau ^ku[nm]i[ng]$ yaaa?",
        "regex": r"^kuning$",
        "success": "Okee yang kuning aja! Aduh aku ^s[ae]n[ao]ng$ banget hari ini bisa ngobrol sama kamu!"
    },
    {
        "day": 1,
        "question": "Okee yang kuning aja! Aduh aku ^s[ae]n[ao]ng$ banget hari ini bisa ngobrol sama kamu!",
        "regex": r"^senang$",
        "success": "Hebat luar biasa kamu berhasil memahami cewe kamu selama seharian!"
    },
    # === DAY 2 ===
    {
        "day": 2,
        "opening": "Sudah saatnya kamu dan dia keluar rumah! Pasti dia bosen #dirumahaja. Hari ini kira kira dia pengennya kemanaa yaa?",
        "question": "Pagi sayangku my love 💌. Semalem aku ^[a-z]idu[rl]$ lamaa banget! Badanku ringan bgt nih",
        "regex": r"^tidur$",
        "success": "^J[ae][mn]$ di kamarku rusak kah? Masih pagi bgt ini..Kamu jg kok udah bangun? Pasti habis mabar sm cwk lain ya.."
    },
    {
        "day": 2,
        "question": "^J[ae][mn]$ di kamarku rusak kah? Masih pagi bgt ini..",
        "regex": r"^Jam$",
        "success": "Anyways, akhirnya paket ^[bp]uk[ui]$ aku udah dateng yipeee"
    },
    {
        "day": 2,
        "question": "Anyways, akhirnya paket ^[bp]uk[ui]$ aku udah dateng yipeee",
        "regex": r"^buku$",
        "success": "Duhh aku laper nihh, kukus ^[def]i[mn]su[mn]$ dulu deh keknya enak"
    },
    {
        "day": 2,
        "question": "Duhh aku laper nihh, kukus ^[def]i[mn]su[mn]$ dulu deh keknya enak",
        "regex": r"^dimsum$",
        "success": "Eh ayang, tau ga si temanku baru pulang dari ^[X-Z]og[i-k][ae]a.arta$ . Keknya seru banget dia healing"
    },
    {
        "day": 2,
        "question": "Eh ayang, tau ga si temanku baru pulang dari ^[X-Z]og[i-k][ae]a.arta$ . Keknya seru banget dia healing",
        "regex": r"^Yogyakarta$",
        "success": "Pengen healing juga aku capek liat tugas semester 5 😥. Kalo besok ke ^t[ae][mn]a[mn]$ buat piknik gimana yang?"
    },
    {
        "day": 2,
        "question": "Pengen healing juga aku capek liat tugas semester 5 😥. Kalo besok ke ^t[ae][mn]a[mn]$ buat piknik gimana yang?",
        "regex": r"^taman$",
        "success": "Yey! Aku mau bawa soda dan ^pi[zs]{2}[a-z]$ ! Gimanaa menurut kamu?"
    },
    {
        "day": 2,
        "question": "Yey! Aku mau bawa soda dan ^pi[zs]{2}[a-z]$ ! Gimanaa menurut kamu?",
        "regex": r"^pizza$",
        "success": "Yey i lov u bgt deh ih gemes 🥺",
        "success_type": "received"
    },
    # === DAY 3 ===
    {
        "day": 3,
        "opening": "Yeay kamu udah lolos 2 hari penuh perjuangan. Tapi tantangan belum selesai. Hari ini saatnya jalan bareng dia, dan ingat, satu langkah aja bisa bikin jalanmu berubah jadi jalan buntu… Sudah siap?",
        "opening_chat": "Pagi! Sayanggg udah ready blom buat hari ini 😍?",
        "question": "Oh iya, hari ini kita ke ^[a-z]us[ae]um$ ya yang pweeease 🥺",
        "regex": r"^museum$",
        "success": "Okedeh, aku mau ^[a-z]iap-[a-z]ia[pb]$ dulu ya!"
    },
    {
        "day": 3,
        "question": "Okedeh, aku mau ^[a-z]iap-[a-z]ia[pb]$ dulu yaa!",
        "regex": r"^siap-siap$",
        "success": "Kamu jangan lupa buat pake baju warna ^[mn]a[gjk][aeiou][mn]t[a-z]$ biar kita couple goals🤟"
    },
    {
        "day": 3,
        "question": "Kamu jangan lupa buat pake baju warna ^[mn]a[gjk][aeiou][mn]t[a-z]$ biar kita couple goals🤟",
        "regex": r"^magenta$",
        "success": "Aku udah siap nih. Kamu ^[bp]er[ae]n[gjl][dkt][ae]t$ sekarang ya sayangg, hati-hatii 🥰"
    },
    {
        "day": 3,
        "question": "Aku udah siap nih. Kamu ^[bp]er[ae]n[gjl][dkt][ae]t$ sekarang ya sayangg, hati-hatii 🥰",
        "regex": r"^berangkat$",
        "success": "Ehh udah laper banget nih, ke ^[a-z]ar[klt]e[ago]$ yuk?"
    },
    {
        "day": 3,
        "question": "Ehh udah laper banget nih, ke ^[a-z]ar[klt]e[ago]$ yuk?",
        "regex": r"^warteg$",
        "success": "Eh tapi gimana kalau kita makan ^ket[ou][dp]r[ae][kl]$ ajaa 😋?"
    },
    {
        "day": 3,
        "question": "Eh tapi gimana kalau kita makan ^ket[ou][dp]r[ae][kl]$ ajaa 😋?",
        "regex": r"^ketoprak$",
        "success": "T-tapi aku masih laper yang… Jajanin aku ^s[ae]b[a-z]a[dk]$ dongg 👉👈"
    },
    {
        "day": 3,
        "question": "T-tapi aku masih laper yang… Jajanin aku ^s[ae]b[a-z]a[dk]$ dongg 👉👈",
        "regex": r"^seblak$",
        "success": "Hari ini seru banget! Makasih ya buat hari ini hehe. Habis ini main ^ro[bp]l[ou][a-z]$ gas"
    },
    {
        "day": 3,
        "question": "Hari ini seru banget! Makasih ya buat hari ini hehe. Habis ini main ^ro[bp]l[ou][a-z]$ gas",
        "regex": r"^roblox$",
        "success": "Yeay, makasih my world ❤️",
        "success_type": "received"
    },
    # === DAY 4 ===
    {
        "day": 4,
        "opening": "Woah ga kerasa udah day 4 aja. I’m sure you’ve got the hang of the game, jadi jangan sampai putus ya, cewemu lagi baik hari ini (kayaknya sih baik ya…let’s see 👀)",
        "question": "Morning cayangku, makasih buat kemarin 🌹Hari ini keluar makan yuk? Tapi mau makan ^[dk][ai]m[ae]n[ae]$ yaa?",
        "regex": r"^dimana$",
        "success": "Gatau kenapa hari ini aku happy bgt deh yang. Kayak ^[st]er[bdp][ae]n[gjkl]$ ke langit 🥰"
    },
    {
        "day": 4,
        "question": "Gatau kenapa hari ini aku happy bgt deh yang. Kayak ^[st]er[bdp][ae]n[gjkl]$ ke langit 🥰",
        "regex": r"^terbang$",
        "success": "Berhubung aku baik, aku udah pesenin ^[bp]e[cs]el\\sa[ly][ae][mn]$ buat kamu my love, dimakan ya jangan sampe perut kamu kosong 🥺 Nanti aku cedih klo kamu sakitt"
    },
    {
        "day": 4,
        "question": "Berhubung aku baik, aku udah pesenin ^[bp]e[cs]el\\sa[ly][ae][mn]$ buat kamu my love, dimakan ya jangan sampe perut kamu kosong 🥺 Nanti aku cedih klo kamu sakitt",
        "regex": r"^pecel ayam$",
        "success": "Oiya btw, aku tiba-tiba kepikiran. Kamu inget ga semalem pas kita jalan, kamu ada ^[bd][aeiou][mn]t[a-z]$ cewe di parkiran?"
    },
    {
        "day": 4,
        "question": "Oiya btw, aku tiba-tiba kepikiran. Kamu inget ga semalem pas kita jalan, kamu ada ^[bd][aeiou][mn]t[a-z]$ cewe di parkiran?",
        "regex": r"^bantu$",
        "success": "Tuhkan, dia siapa? Kok kamu malah ^pe[bd][au]l[ai]$ ke cewe lain disaat kita lagi ngedate? Are you out of your mind 😡?!!"
    },
    {
        "day": 4,
        "question": "Tuhkan, dia siapa? Kok kamu malah ^pe[bd][au]l[ai]$ ke cewe lain disaat kita lagi ngedate? Are you out of your mind 😡?!!",
        "regex": r"^peduli$",
        "success": "Aku ^c[eu][mn][bp]u[lr][au]$ tau ga….Tega bgt kamu yang…."
    },
    {
        "day": 4,
        "question": "Aku ^c[eu][mn][bp]u[lr][au]$ tau ga….Tega bgt kamu yang….",
        "regex": r"^cemburu$",
        "success": "Jujur aja, pasti kamu ^s[ae][kl]in[a-z]k[aeiou][hj]$ . Hati mungilku gabisa banget diginiin 💔."
    },
    {
        "day": 4,
        "question": "Jujur aja, pasti kamu ^s[ae][kl]in[a-z]k[aeiou][hj]$ . Hati mungilku gabisa banget diginiin 💔.",
        "regex": r"^selingkuh$",
        "success": "Ah aku nangis kan….padahal tadi happy. Udahlah aku mau cool off dulu. Bye world",
        "success_type": "received"
    },
    # === DAY 5 ===
    {
        "day": 5,
        "opening": "Welcome to the last and most thrilling day. Di last day ini kamu bakal ngelanjutin konflik, jadi make sure kamu ga salah jawab biar ga putus. Are u ready kids 😋?",
        "question": "Pagi.. ^[A-Z]ar[ae][bp]a[mn]$ apa 🙄?",
        "regex": r"^Sarapan$",
        "success": "Aku mau ngomong serius deh . Aku ngerasa belakangan ini kamu ^[a-z]u[aei][kl]$. Kamu kalo ada masalah ngomong lah jgn diem aja…ngajak berantem 🤬?!"
    },
    {
        "day": 5,
        "question": "Aku mau ngomong serius deh . Aku ngerasa belakangan ini kamu ^[a-z]u[aei][kl]$.",
        "regex": r"^cuek$",
        "success": "Aku gangerti ya, ntah kamu selingkuh atau kamu udah bosen aja sama aku... Yaudah, kalau gitu ^[retsah]8$ , aku gamau peduli lagi 😒"
    },
    {
        "day": 5,
        "question": "Aku gangerti ya, ntah kamu selingkuh atau kamu udah bosen aja sama aku... Yaudah, kalau gitu ^[retsah]8$ , aku gamau peduli lagi 😒",
        "regex": r"^terserah$",
        "success": "Inget ga 2 minggu lalu aku ajak kamu main ^[bp]a[bd][ae][ls]$ , tapi kamu nolak, trus feedsku jadi kalah estetik dari temenku 💔"
    },
    {
        "day": 5,
        "question": "Inget ga 2 minggu lalu aku ajak kamu main ^[bp]a[bd][ae][ls]$ , tapi kamu nolak, trus feedsku jadi kalah estetik dari temenku 💔",
        "regex": r"^padel$",
        "success": "Terus, 3 minggu lalu, aku ajak ke cafe specialty ^m[aei][stu]c[a-z][aei]$ kamu gamau juga….emang aku udah gapenting ya dihidupmu?!!!!!"
    },
    {
        "day": 5,
        "question": "Terus, 3 minggu lalu, aku ajak ke cafe specialty ^m[aei][stu]c[a-z][aei]$ kamu gamau juga….emang aku udah gapenting ya dihidupmu?!!!!!",
        "regex": r"^matcha$",
        "success": "Kemarin kamu bilang aku cantik kayak ^[bdp]u[jkl]a[mn]$... itu semua apa artinya? Kamu bisanya main-main sama perasaanku doang"
    },
    {
        "day": 5,
        "question": "Kemarin kamu bilang aku cantik kayak ^[bdp]u[jkl]a[mn]$... itu semua apa artinya? Kamu bisanya main-main sama perasaanku doang",
        "regex": r"^bulan$",
        "success": "Yaudah gini aja, kalau kamu mau beliin aku ^t[eio][jkl]u[a-z]\\s[dgr][au][bdl][au]n[a-z]$ , kita baikan.",
        "interlude": "Hummmph kesel banget deh sama kamu, tapi aku masih sayang juga.. Akutuh gabisa diginiin 🥹"
    },
    {
        "day": 5,
        "question": "Yaudah gini aja, kalau kamu mau beliin aku ^t[eio][jkl]u[a-z]\\s[dgr][au][bdl][au]n[a-z]$ , kita baikan.",
        "regex": r"^telur gulung$",
        "success": "Aduh aku tersipu bgt kamu top deh bisa ngerti apa yang aku bilang. I love you my hunny bunny maaf ya udah marah-marah 🥺"
    },
]

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/rules")
def rules():
    return render_template("rules.html")
    
@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/chat")
def chat():
    session['lives'] = 3
    session['level'] = 0
    return render_template("chat.html")

@app.route('/api/start_game', methods=['GET'])
def start_game():
    session.clear()
    session['lives'] = 3
    session['level'] = 0
    first_level = GAME_LEVELS[0]
    return jsonify({
        "lives": session['lives'],
        "opening": first_level.get("opening"),
        "question": first_level.get("question"),
        "day": first_level.get("day", 1)
    })

@app.route('/api/next_question', methods=['GET'])
def next_question():
    level = session.get('level', 0)
    if level < len(GAME_LEVELS):
        next_level_data = GAME_LEVELS[level]
        return jsonify({
            "opening": next_level_data.get("opening"),
            "opening_chat": next_level_data.get("opening_chat"),
            "question": next_level_data.get("question"),
            "day": next_level_data.get("day")
        })
    return jsonify({"status": "error", "message": "Game sudah selesai!"})

@app.route('/api/validate', methods=['POST'])
def validate_answer():
    data = request.json
    user_answer = data.get('answer', '').lower()
    level = session.get('level', 0)
    lives = session.get('lives', 3)

    if level >= len(GAME_LEVELS):
        return jsonify({"status": "error", "message": "Game sudah selesai, silakan refresh."})

    current_level_data = GAME_LEVELS[level]
    
    if re.match(current_level_data['regex'], user_answer, re.IGNORECASE):
        level += 1
        session['level'] = level
        
        if level >= len(GAME_LEVELS):
            return jsonify({
                "status": "win",
                "final_dialogue": current_level_data['success'],
                "win_message": WIN_MESSAGE
            })

        next_level_data = GAME_LEVELS[level]
        is_day_over = next_level_data.get('day') != current_level_data.get('day')

        if is_day_over:
            return jsonify({
                "status": "day_complete",
                "message": current_level_data['success'],
                "day": next_level_data.get("day"),
                "success_type": current_level_data.get("success_type", "notification")
            })
        else:
            return jsonify({
                "correct": True,
                "message": next_level_data['question'],
                "lives": lives,
                "interlude": current_level_data.get("interlude")
            })
    else:
        lives -= 1
        session['lives'] = lives
        if lives > 0:
            return jsonify({
                "correct": False,
                "message": "Hah? Kok gitu jawabnya? Coba lagi deh...",
                "lives": lives
            })
        else:
            game_over_msg = random.choice(GAME_OVER_MESSAGES)
            return jsonify({
                "status": "game_over",
                "message": game_over_msg,
                "lives": 0
            })

if __name__ == '__main__':
    app.run(debug=False)