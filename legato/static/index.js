function like(postId) {
  // Get counter-${postId} element and store it in the counter variable
  const counter = document.getElementById(`counter-${postId}`);
  // Get dislike-button-${postId} element and store it in the dislikeButton variable
  const likeButton = document.getElementById(`like-button-${postId}`);
  // Get like-button-${postId} element and store it in the `likeButton` variable
  const dislikeButton = document.getElementById(`dislike-button-${postId}`);
  // Send a POST request to /dislike-post/${postId} using fetch
  fetch(`/like-post/${postId}`, { method: "POST" })
    // Once the response is received, parse the response body as JSON and store it in the data variable
    .then((res) => res.json())
    // Update the HTML counter element with the value of the votes key in the data object
    .then((data) => {
      counter.innerHTML = data["votes"];
      if (data["liked"] === true) {
        // Change the class of the likeButton and dislikeButton based on the liked key in the data object
        likeButton.className = "fa-solid fa-volume-high";
        dislikeButton.className = "fa-solid fa-volume-off";
      } else {
        likeButton.className = "fa-solid fa-volume-low";
      }
    })
    .catch((e) => alert("Could not like post."));
}

function dislike(postId) {
  // Get counter-${postId} element and store it in the counter variable
  const counter = document.getElementById(`counter-${postId}`);
  // Get dislike-button-${postId} element and store it in the dislikeButton variable
  const dislikeButton = document.getElementById(`dislike-button-${postId}`);
  // Get like-button-${postId} element and store it in the likeButton variable
  const likeButton = document.getElementById(`like-button-${postId}`);
  // Send a POST request to /dislike-post/${postId} using fetch
  fetch(`/dislike-post/${postId}`, { method: "POST" })
    // Once the response is received, parse the response body as JSON and store it in the data variable
    .then((res) => res.json())
    // Update the HTML counter element with the value of the votes key in the data object
    .then((data) => {
      counter.innerHTML = data["votes"];
      if (data["disliked"] === true) {
        // Change the class of the dislikeButton and likeButton based on the disliked key in the data object
        dislikeButton.className = "fa-solid fa-volume-xmark";
        likeButton.className = "fa-solid fa-volume-low";
      } else {
        dislikeButton.className = "fa-solid fa-volume-off";
      }
    })
    // If an error occurs, display an alert message to the user
    .catch((e) => alert("Could not dislike post."));
}
