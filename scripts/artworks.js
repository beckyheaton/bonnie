fetch('artwork_indexing/artworks.json')
    .then(res => res.json())
    .then(artworks => {
        const container = document.getElementById('artworks');

        artworks.forEach(art => {
            const tile = document.createElement('div');
            tile.className = 'artwork-tile';

            tile.innerHTML = `
                <div class="artwork-image-wrap">
                    <img src="${art.thumbnail}" alt="${art.name}">
                </div>
                <p class="artwork-name">${art.name}</p>
            `;

            tile.addEventListener('click', () => {
                window.location.href = `artwork.html?id=${art.id}`;
            });

            container.appendChild(tile);
        });
    });