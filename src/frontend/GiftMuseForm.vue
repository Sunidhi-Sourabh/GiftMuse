fetch("http://localhost:8080/generate-bundle", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(formData)
})
.then(res => res.json())
.then(data => {
  // Redirect to /giftmuse-result and pass bundle data
})
