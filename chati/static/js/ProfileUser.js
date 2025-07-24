let currentPage = 1;
let isLoading = false;

window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200 && !isLoading) {
        isLoading = true;
        currentPage++;

        fetch(`/profile/?page=${currentPage}`, {
            headers: {
                'x-requested-with': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.posts.length > 0) {
                const feedContainer = document.getElementById('PUfeed');

                data.posts.forEach(post => {
                    const postDiv = document.createElement('div');
                    postDiv.classList.add('PUpost');

                    postDiv.innerHTML = `
                        <div class="PUpost-header">
                            <div class="PUUserPhoto" style="background-image: url('${post.profile_picture_url || "/static/images/DefaultHeader.png"}')"></div>
                            <div class="PUUserInfo">
                                <strong class="PUpostUser">${post.first_name} ${post.last_name}</strong>
                                <span class="PUpostUserdate"> · ${post.post_date}</span>
                            </div>
                        </div>
                        <p class="PUpost-content">${post.text_content}</p>
                        ${post.media_url ? `<div class="PUpost-media" style="background-image: url('${post.media_url}')"></div>` : ''}
                        <div class="PUpost-actions">
                            <span class="comments">
                                <img src="/static/images/Chat.png" alt="Comentarios" class="icon">
                                <span class="count">${post.comment_count}</span>
                            </span>
                            <span class="likes">
                                <img src="/static/images/Heart.png" alt="Me gusta" class="icon">
                                <span class="count">0</span>
                            </span>
                            <span class="share">
                                <img src="/static/images/Share.png" alt="Compartir" class="icon">
                                <span class="count">0</span>
                            </span>
                        </div>
                        ${post.comments.length > 0 ? `
                        <div class="PUcomments-section">
                            ${post.comments.map(c => `<div class="PUcomment"><strong>${c.user}:</strong> ${c.content}</div>`).join('')}
                            ${post.comment_count > 3 ? `<div class="PUview-more">Ver ${post.comment_count - 3} comentarios más...</div>` : ''}
                        </div>
                        ` : ''}
                    `;

                    feedContainer.appendChild(postDiv);
                });

                isLoading = false;
            }
        })
        .catch(error => {
            console.error('Error cargando publicaciones:', error);
        });
    }
});
