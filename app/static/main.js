//  Toggle comment visibility
function toggleComments(postId) {
  const commentsSection = document.getElementById(`comments-${postId}`);
  const toggleButton = document.getElementById(`toggle-btn-${postId}`);
  const commentIcon = document.getElementById(`comment-icon-${postId}`);

  if (commentsSection.style.display === "none" || commentsSection.style.display === "") {
    commentsSection.style.display = "block";
  } else {
    commentsSection.style.display = "none";
  }
}

// Dropdown menu
function toggleOptionsDropdown(postId) {
  const optionsDropdown = document.getElementById(`options-dropdown-${postId}`);
  optionsDropdown.style.display = optionsDropdown.style.display === "block" ? "none" : "block";
}

document.addEventListener("DOMContentLoaded", () => {
  
  // Edit post
  document.querySelectorAll(".edit-post-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const postId = button.dataset.postId;
      const postContentElement = document.querySelector(`#post-content-${postId}`);
      const newContent = prompt("Edit your post:", postContentElement.textContent);

      if (newContent) {
        fetch(`/edit_post/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: newContent }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              postContentElement.textContent = data.new_content;
            } else {
              alert(data.message);
            }
          })
          .catch((error) => console.error("Error editing post:", error));
      }
    });
  });

  // Edit comment
  document.querySelectorAll(".edit-comment-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const commentId = button.dataset.commentId;
      const commentContentElement = document.querySelector(`#comment-content-${commentId}`);
      const newContent = prompt("Edit your comment:", commentContentElement.textContent);

      if (newContent) {
        fetch(`/edit_comment/${commentId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: newContent }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              commentContentElement.textContent = data.new_content;
            } else {
              alert(data.message);
            }
          })
          .catch((error) => console.error("Error editing comment:", error));
      }
    });
  });
});

// Liking posts via AJAX
document.addEventListener("DOMContentLoaded", () => {
  const likeButtons = document.querySelectorAll(".like-btn");

  likeButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      const postId = button.dataset.postId;
      const likeCountSpan = document.querySelector(`#like-count-${postId}`);

      fetch(`/like_post/${postId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            likeCountSpan.textContent = `${data.like_count} ${
              data.like_count === 1 ? "Like" : "Likes"
            }`;
          }
        })
        .catch((error) => {
          console.error("Error liking post:", error);
        });
    });
  });
});
