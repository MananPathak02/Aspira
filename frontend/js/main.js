// Scroll reveal animation
document.addEventListener("scroll", () => {
  const items = document.querySelectorAll(".scroll-item");
  items.forEach(item => {
    const rect = item.getBoundingClientRect();
    if (rect.top < window.innerHeight - 100) {
      item.classList.add("visible");
    }
  });
});
