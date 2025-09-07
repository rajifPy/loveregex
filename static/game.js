const GAME_OVER_MESSAGES = [
    "Emang kamu gapernah ngertiin aku. Semua ini kayak game aja buat kamu. Kita PUTUSS! 🤬",
    "Kamu sayang ga sih sama aku? Disuruh ngertiin regex doang kok susah bgt… KITA PUTUS AJA!!"
];

const WIN_MESSAGE = "SELAMAT! Kamu berhasil mencapai akhir cerita.<br><br>Kamu telah belajar bahasa cinta yang paling unik: Regex. Setiap pola yang kamu tebak bukan hanya barisan kode, tapi juga bukti kesabaran dan pengertianmu.<br><br>Hubunganmu kini lebih kuat dari sebelumnya. Kalian berhasil! 💖";

const GAME_LEVELS = [
    // Paste SELURUH array GAME_LEVELS dari app.py Anda di sini (sama persis, termasuk regex sebagai string)
    // Contoh: { "day": 1, "opening": "...", ... },
    // ... (semua levels)
];

let lives = 3;
let level = 0;

// Fungsi untuk tampilkan pesan di chat area (asumsi ada <div id="chat-area"></div> di chat.html)
function displayMessage(message, type = 'question') {
    const chatArea = document.getElementById('chat-area');
    const p = document.createElement('p');
    p.innerHTML = message;
    p.classList.add(type);  // Bisa style dengan CSS: .question { color: blue; } dll.
    chatArea.appendChild(p);
    chatArea.scrollTop = chatArea.scrollHeight;
}

// Start game
function startGame() {
    lives = 3;
    level = 0;
    document.getElementById('chat-area').innerHTML = '';  // Clear chat
    const firstLevel = GAME_LEVELS[0];
    if (firstLevel.opening) displayMessage(firstLevel.opening, 'opening');
    displayMessage(firstLevel.question, 'question');
    document.getElementById('lives').textContent = lives;  // Asumsi ada <span id="lives"></span>
    document.getElementById('day').textContent = firstLevel.day;  // Asumsi ada <span id="day"></span>
}

// Validate jawaban
function validateAnswer() {
    const input = document.getElementById('answer-input');
    const userAnswer = input.value.trim().toLowerCase();
    input.value = '';  // Clear input

    if (!userAnswer) return;

    const currentLevel = GAME_LEVELS[level];
    const regex = new RegExp(currentLevel.regex, 'i');  // Case-insensitive

    if (regex.test(userAnswer)) {
        level++;
        if (level >= GAME_LEVELS.length) {
            displayMessage(currentLevel.success, 'success');
            displayMessage(WIN_MESSAGE, 'win');
            return;
        }
        const nextLevel = GAME_LEVELS[level];
        const isDayOver = nextLevel.day !== currentLevel.day;

        if (currentLevel.interlude) displayMessage(currentLevel.interlude, 'interlude');

        if (isDayOver) {
            displayMessage(currentLevel.success, currentLevel.success_type || 'notification');
            // Optional: Tombol untuk lanjut hari baru
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Lanjut ke Day ' + nextLevel.day;
            nextBtn.onclick = () => {
                if (nextLevel.opening) displayMessage(nextLevel.opening, 'opening');
                if (nextLevel.opening_chat) displayMessage(nextLevel.opening_chat, 'opening_chat');
                displayMessage(nextLevel.question, 'question');
                document.getElementById('day').textContent = nextLevel.day;
                nextBtn.remove();
            };
            document.getElementById('chat-area').appendChild(nextBtn);
        } else {
            displayMessage(nextLevel.question, 'question');
        }
    } else {
        lives--;
        document.getElementById('lives').textContent = lives;
        if (lives > 0) {
            displayMessage("Hah? Kok gitu jawabnya? Coba lagi deh...", 'error');
        } else {
            const gameOverMsg = GAME_OVER_MESSAGES[Math.floor(Math.random() * GAME_OVER_MESSAGES.length)];
            displayMessage(gameOverMsg, 'game_over');
        }
    }
}

// Event listeners (panggil ini di onload)
document.addEventListener('DOMContentLoaded', () => {
    startGame();
    document.getElementById('submit-btn').addEventListener('click', validateAnswer);
    document.getElementById('answer-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') validateAnswer();
    });
});