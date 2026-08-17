// Wedding Date & Time: September 14, 2026, 06:00:00 (Local Time)
// Note: In JavaScript, months are 0-indexed. September is month index 8.
const TARGET_DATE = new Date(2026, 8, 14, 6, 0, 0);

function updateCountdown() {
  const now = new Date();
  const diffMs = TARGET_DATE - now;

  if (diffMs <= 0) {
    document.getElementById("days").innerText = "00";
    document.getElementById("hours").innerText = "00";
    document.getElementById("minutes").innerText = "00";
    document.getElementById("seconds").innerText = "00";
    return;
  }

  // Time calculations
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);

  // Formatting with padding leading zeros
  document.getElementById("days").innerText = String(days).padStart(2, "0");
  document.getElementById("hours").innerText = String(hours).padStart(2, "0");
  document.getElementById("minutes").innerText = String(minutes).padStart(2, "0");
  document.getElementById("seconds").innerText = String(seconds).padStart(2, "0");
}

// Start ticking
updateCountdown();
setInterval(updateCountdown, 1000);

// Sharing functionality using the Web Share API (native sheet)
async function shareInvitation() {
  const shareData = {
    title: "Wedding Invitation",
    text: "You are warmly invited to celebrate with us. Please join us for our wedding celebration.",
    url: window.location.href
  };

  try {
    if (navigator.share) {
      await navigator.share(shareData);
      console.log("Invitation shared successfully!");
    } else {
      // Fallback: Copy URL to clipboard
      await navigator.clipboard.writeText(window.location.href);
      alert("Invitation link copied to clipboard! You can paste and share it with your friends.");
    }
  } catch (err) {
    console.log("Error sharing or copying invitation:", err);
  }
}

// Image Zoom Modal Functions
const modal = document.getElementById("zoomModal");
const modalImg = document.getElementById("zoomedImg");

function openZoom(imageSrc) {
  modal.style.display = "flex";
  modalImg.src = imageSrc;
}

function closeZoom() {
  modal.style.display = "none";
}

// Close modal when pressing the Esc key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeZoom();
  }
});

// Intersection Observer for scroll-reveal animations (painting effect)
document.addEventListener("DOMContentLoaded", () => {
  const profileWrappers = document.querySelectorAll(".profile-card .image-wrapper");
  
  const observerOptions = {
    root: null,
    rootMargin: "0px 0px -120px 0px", // Trigger when element is 120px inside viewport
    threshold: 0.05
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("reveal");
        observer.unobserve(entry.target); // Reveal animation only triggers once
      }
    });
  }, observerOptions);

  profileWrappers.forEach(wrapper => {
    observer.observe(wrapper);
  });
});
