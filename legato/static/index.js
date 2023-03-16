function like(postId) {
  const counter = document.getElementById(`counter-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);
  const dislikeButton = document.getElementById(`dislike-button-${postId}`);

  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      counter.innerHTML = data["votes"];
      if (data["liked"] === true) {
        likeButton.className = "fa-solid fa-volume-high";
        dislikeButton.className = "fa-solid fa-volume-off";
      } else {
        likeButton.className = "fa-solid fa-volume-low";
      }
    })
    .catch((e) => alert("Could not like post."));
}

function dislike(postId) {
  const counter = document.getElementById(`counter-${postId}`);
  const dislikeButton = document.getElementById(`dislike-button-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);
  fetch(`/dislike-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      counter.innerHTML = data["votes"];
      if (data["disliked"] === true) {
        dislikeButton.className = "fa-solid fa-volume-xmark";
        likeButton.className = "fa-solid fa-volume-low";
      } else {
        dislikeButton.className = "fa-solid fa-volume-off";
      }
    })
    .catch((e) => alert("Could not dislike post."));
}
