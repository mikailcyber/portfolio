const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("show");
    menuToggle.setAttribute("aria-expanded", String(navLinks.classList.contains("show")));
  });
}

// Keep the portable portfolio useful if an older project video was not supplied.
function showMissingVideo(video) {
  if (video.dataset.missingVideoShown) return;
  video.dataset.missingVideoShown = 'true';
  video.hidden = true;
  const note = document.createElement('p');
  note.textContent = 'Deze video is niet meegeleverd in dit portfolio-exemplaar. De beschrijving en afbeeldingen van het project staan op deze pagina.';
  note.setAttribute('role', 'status');
  video.insertAdjacentElement('afterend', note);
}
document.querySelectorAll('video').forEach((video) => {
  video.addEventListener('error', () => showMissingVideo(video));
  video.querySelectorAll('source').forEach((source) => {
    source.addEventListener('error', () => showMissingVideo(video));
  });
  if (video.error) showMissingVideo(video);
});
