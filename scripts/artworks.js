fetch('artwork_indexing/artworks.json')
    .then(res => res.json())
    .then(artworks => {
        const container = document.getElementById('artworks');

        // newest first
        const sorted = [...artworks].sort((a, b) => new Date(b.date) - new Date(a.date));

        sorted.forEach(art => {
            const row = document.createElement('div');
            row.className = 'artwork-row';

            row.innerHTML = `
                <span class="artwork-date">${art.date ?? ''}</span>
                <span class="artwork-name">${art.name}</span>
                <img class="artwork-icon" src="${art.thumbnail}" alt="">
            `;

            row.addEventListener('click', () => {
                window.location.href = `artwork.html?id=${art.id}`;
            });

            container.appendChild(row);
        });
    });