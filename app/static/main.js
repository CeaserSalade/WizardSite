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

function toggleOptionsDropdown(postId) {
  const optionsDropdown = document.getElementById(`options-dropdown-${postId}`);
  optionsDropdown.style.display = optionsDropdown.style.display === "block" ? "none" : "block";
}
