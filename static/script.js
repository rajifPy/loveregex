// static/script.js (Versi Final yang Sudah Diperbaiki dan Dirapikan)

// === Variabel Global ===
const heartImage = document.getElementById('heart-image');
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const clickSound = document.getElementById('click-sound');
const sendSound = document.getElementById('send-sound');
const receiveSound = document.getElementById('receive-sound');

const heartImages = [
    "/static/assets/bar5.png", // 0 nyawa
    "/static/assets/bar4.png", // 1 nyawa
    "/static/assets/bar2.png", // 2 nyawa
    "/static/assets/bar1.png"  // 3 nyawa
];

// === Fungsi Helper ===
function playClickSound() {
    if (clickSound) {
        clickSound.currentTime = 0;
        clickSound.volume = 1;
        clickSound.play();
    }
}

function playSendSound() {
    if (sendSound) {
        sendSound.currentTime = 0;
        sendSound.play();
    }
}

function playReceiveSound() {
    if (receiveSound) {
        receiveSound.currentTime = 0;
        receiveSound.play();
    }
}

function updateHeartBar(currentLives) {
    const index = Math.max(0, Math.min(currentLives, heartImages.length - 1));
    heartImage.src = heartImages[index];
}

function addMessage(text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.innerHTML = text;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function disableInput() {
    chatInput.disabled = true;
    sendBtn.disabled = true;
    chatInput.placeholder = "Game Selesai atau menunggu...";
}

function enableInput() {
    chatInput.disabled = false;
    sendBtn.disabled = false;
    chatInput.placeholder = "Ketik di sini... (Enter untuk kirim)";
    chatInput.focus();
}

function showEndGameButton(status) {
    // 1. Buat kontainer untuk tombol
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('end-game-buttons');

    // 2. Buat Tombol 1 (Main Lagi / Coba Lagi)
    const btnRestart = document.createElement('button');
    btnRestart.classList.add('restart-btn');
    if (status === 'win') {
        btnRestart.textContent = 'Main Lagi?';
        btnRestart.classList.add('btn-win');
    } else {
        btnRestart.textContent = 'Kasih Kesempatan Kedua';
        btnRestart.classList.add('btn-lose');
    }
    btnRestart.onclick = () => {
        playClickSound();
        window.location.reload(); // Muat ulang halaman chat
    };

    // 3. Buat Tombol 2 (Kembali ke Awal)
    const btnHome = document.createElement('button');
    btnHome.textContent = 'Kembali ke Awal';
    btnHome.classList.add('restart-btn', 'btn-home'); // Terapkan gaya dasar & warna ungu
    btnHome.onclick = () => {
        playClickSound();
        window.location.href = "/"; // Arahkan ke halaman landing
    };

    // 4. Masukkan kedua tombol ke dalam kontainer
    buttonContainer.appendChild(btnRestart);
    buttonContainer.appendChild(btnHome);

    // 5. Tampilkan kontainer di jendela chat
    chatWindow.appendChild(buttonContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showNextDayButton(successMessage, successType) {
    const btn = document.createElement('button');
    btn.textContent = 'Lanjut ke Hari Berikutnya';
    btn.classList.add('restart-btn', 'btn-win'); // Selalu hijau

    btn.onclick = async () => {
        playClickSound();
        chatWindow.innerHTML = '';
        try {
            const response = await fetch('/api/next_question');
            const data = await response.json();
            
            addMessage(`<strong>DAY ${data.day}</strong>`, 'day-indicator');

            if (data.opening) {
                addMessage(data.opening, 'notification');
                playReceiveSound();
            }

            // --- LOGIKA BARU UNTUK BUBBLE BERURUTAN ---
            if (data.opening_chat) {
                // Tampilkan bubble pertama setelah 1 detik
                setTimeout(() => {
                    addMessage(data.opening_chat, 'received');
                    playReceiveSound();
                }, 1000);

                // Tampilkan bubble kedua (pertanyaan) setelah 2.5 detik
                setTimeout(() => {
                    if (data.question) {
                        addMessage(data.question, 'received');
                        playReceiveSound();
                        enableInput(); // Aktifkan input setelah pertanyaan terakhir muncul
                    }
                }, 2500);
            } else {
                // Logika lama untuk hari-hari lain yang tidak punya opening_chat
                if (data.question) {
                    setTimeout(() => {
                        addMessage(data.question, 'received');
                        playReceiveSound();
                        enableInput();
                    }, data.opening ? 1000 : 0);
                }
            }
        } catch (error) {
            console.error("Gagal mengambil pertanyaan berikutnya:", error);
            addMessage("Gagal memuat hari berikutnya.", 'received');
        }
    };
    
    const messageType = successType || 'notification';
    addMessage(successMessage, messageType);
    playReceiveSound();
    chatWindow.appendChild(btn);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// === Logika Inti Game ===
async function sendMessage() {
    const message = chatInput.value.trim();
    if (message === '' || chatInput.disabled) return;
    
    addMessage(message, 'sent');
    playSendSound();
    playClickSound();
    chatInput.value = '';

    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer: message }),
        });
        const data = await response.json();
        
        setTimeout(() => {
            if (data.status === 'day_complete') {
                disableInput();
                showNextDayButton(data.message, data.success_type);

            } else if (data.status === 'game_over') {
                updateHeartBar(data.lives);
                addMessage(data.message, 'received');
                playReceiveSound();
                disableInput();
                showEndGameButton('lose'); // <-- PERBAIKAN 1

            } else if (data.status === 'win') {
                // <-- PERBAIKAN 2 (Logika Win)
                addMessage(data.final_dialogue, 'received'); // Tampilkan dialog terakhir dulu
                playReceiveSound();
                disableInput();
                
                setTimeout(() => {
                    addMessage(data.win_message, 'notification');
                    playReceiveSound();
                }, 1500);

                setTimeout(() => {
                    showEndGameButton('win');
                }, 3000);

            } else if (data.correct === true) {
                if (data.interlude) {
                    // Tampilkan dialog perantara terlebih dahulu
                    addMessage(data.interlude, 'received');
                    playReceiveSound();
                    disableInput(); // Nonaktifkan input sementara

                    // Tampilkan pertanyaan berikutnya setelah jeda
                    setTimeout(() => {
                        addMessage(data.message, 'received');
                        playReceiveSound();
                        enableInput(); // Aktifkan lagi inputnya
                    }, 2000); // Jeda 2 detik
                } else {
                    // Jika tidak ada interlude, jalankan seperti biasa
                    addMessage(data.message, 'received');
                    playReceiveSound();
                }

            } else { // Jawaban salah
                addMessage(data.message, 'received');
                playReceiveSound();
                if (data.lives !== undefined) {
                    updateHeartBar(data.lives);
                }
            }
        }, 500);
    } catch (error) {
        console.error("Gagal menghubungi server:", error);
        addMessage("Duh, koneksi ke server lagi bermasalah nih.", 'received');
    }
}

async function initializeGame() {
    try {
        const response = await fetch('/api/start_game');
        const data = await response.json();
        
        addMessage(`<strong>DAY ${data.day}</strong>`, 'day-indicator');
        updateHeartBar(data.lives);

        if (data.opening) {
            addMessage(data.opening, 'notification');
            playReceiveSound();
        }
        setTimeout(() => {
            if (data.question) {
                addMessage(data.question, 'received');
                playReceiveSound();
            }
        }, data.opening ? 1000 : 0);
    } catch (error) {
        console.error("Gagal memulai game:", error);
        addMessage("Gagal memuat game. Coba refresh halaman.", 'received');
    }
}

// === Event Listeners & Inisialisasi ===
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});
document.addEventListener('DOMContentLoaded', initializeGame);