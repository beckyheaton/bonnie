const params = new URLSearchParams(window.location.search);
const id = params.get('id');

fetch('artwork_indexing/artworks.json')
    .then(res => res.json())
    .then(artworks => {
        const art = artworks.find(a => a.id === id);
        if (!art) { document.body.innerHTML = '<p>Artwork not found.</p>'; return; }

        const container = document.getElementById('artwork-page');
        let mainContent = '';

        if (art.type.includes('video') && art.videoLink) {
            const videoId = art.videoLink.split('youtu.be/')[1];
            mainContent = `<iframe width="560" height="315"
                src="https://www.youtube.com/embed/${videoId}"
                frameborder="0" allowfullscreen></iframe>`;

        } else if (art.type.includes('text') && art.documentLink) {
            fetch(art.documentLink)
                .then(r => r.text())
                .then(text => {
                    document.getElementById('main').innerText = text;
                });
            mainContent = `<pre id="main"></pre>`;

        } else {
            mainContent = `<img src="${art.thumbnail}" alt="${art.name}">`;
        }

        container.innerHTML = `
            <p>${art.name}</p>
            <p>${art.date ?? ''}</p>
            ${mainContent}
            <p>${art.description ?? ''}</p>
        `;
    });