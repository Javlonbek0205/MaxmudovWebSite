
// Function to update main image when clicking thumbnails
function updateMainImage(src) {
    document.getElementById('mainImage').src = src;
}

// Add smooth scrolling for comments
document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.querySelector('.comment-form');

    if (commentForm) {
        commentForm.addEventListener('submit', function() {
            // Show loading state if needed
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...';
            }
        });
    }

    // Handle like button animation
    const likeForm = document.querySelector('.like-form');
    if (likeForm) {
        likeForm.addEventListener('submit', function(e) {
            const likeButton = this.querySelector('.like-button');
            if (likeButton) {
                likeButton.classList.add('animate-like');
                setTimeout(() => {
                    likeButton.classList.remove('animate-like');
                }, 1000);
            }

        });
    }
});

function toggleComments() {
    const container = document.querySelector('.comments-container');
    const button = document.querySelector('.toggle-comments');
    const icon = button.querySelector('i');

    container.classList.toggle('show');
    button.classList.toggle('active');
}