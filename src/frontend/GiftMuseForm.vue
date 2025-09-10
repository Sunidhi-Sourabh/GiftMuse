fetch("http://<giftmuse-agent-service>/generate-bundle", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    occasion: "...",
    recipient_gender: "...",
    relation: "...",
    budget: "...",
    rating: "...",
    likes: "...",
    dislikes: "..."
  })
})
.then(res => res.json())
.then(data => {
  // Redirect to /giftmuse-result and show the bundle
})
