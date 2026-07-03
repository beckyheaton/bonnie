const params = new URLSearchParams(window.location.search);
const id = params.get('id');

fetch('artwork_indexing/artworks.json')
    .then(res => res.json())
    .then(artworks => {
        const art = artworks.find(a => a.id === id);
        if (!art) { document.getElementById('artwork-page').innerHTML = '<p>Artwork not found.</p>'; return; }

        const isVideo = art.type.includes('video') && art.videoLink;
        const videoId = isVideo ? art.videoLink.split('youtu.be/')[1].split('?')[0] : null;

        const media = isVideo
            ? `<iframe src="https://www.youtube.com/embed/${videoId}" allowfullscreen></iframe>`
            : `<img src="${art.thumbnail}" alt="${art.name}">`;

        document.getElementById('artwork-page').innerHTML = `
            <h1 class="artwork-title">${art.name}</h1>
            <div class="artwork-content">
                <div class="artwork-media">${media}</div>
                <p class="artwork-description">${art.description ?? ''}</p>
            </div>
        `;
    });