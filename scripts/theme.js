const current = localStorage.getItem('theme') || 'sky';
const next = current === 'sky' ? 'ocean' : 'sky';

const bubbleSound = new Audio('assets/sounds/stream.mp3');
bubbleSound.loop = true;
if (current === 'ocean') {
    bubbleSound.play();
}

const bgImages = {
    sky: 'assets/images/skyLong.jpg',
    ocean: 'assets/images/oceanComputer.png'
};

const preload = new Image();
preload.src = bgImages[current];
preload.decode().then(() => {
    document.body.classList.add(`theme-${current}`);
    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });
});

const script = document.createElement('script');
script.src = current === 'sky' ? 'scripts/tinkerbellMagicSparkle.js' : 'scripts/bubbleCursor.js';
document.body.appendChild(script);

const button = document.getElementById('theme-toggle');
button.textContent = next;
button.addEventListener('click', () => {
    localStorage.setItem('theme', next);
    document.body.style.opacity = '0';
    setTimeout(() => location.reload(), 1200);
});