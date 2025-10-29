// === ANIMASI MASUK HALAMAN ===
document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("page-enter");
    setTimeout(() => {
        document.body.classList.add("page-enter-active");
    }, 10);
});

// === ANIMASI TRANSISI SAAT PINDAH HALAMAN ===
const links = document.querySelectorAll("a");

links.forEach(link => {
    link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("http")) return;
        e.preventDefault();
        document.body.classList.add("page-exit");
        setTimeout(() => {
            window.location.href = href;
        }, 400);
    });
});

// === EFEK HOVER DAN KLIK UNTUK TOMBOL ===
const buttons = document.querySelectorAll(".btn, .btn-back");

buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
        btn.style.boxShadow = "0 0 25px rgba(0, 224, 255, 0.9)";
        btn.style.transform = "scale(1.1)";
    });
    btn.addEventListener("mouseleave", () => {
        btn.style.boxShadow = "0 0 10px rgba(0, 224, 255, 0.4)";
        btn.style.transform = "scale(1)";
    });
    btn.addEventListener("click", () => {
        btn.style.transform = "scale(0.95)";
        setTimeout(() => (btn.style.transform = "scale(1.05)"), 150);
    });
});

// === EFEK SCROLL FADE-IN ===
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
        }
    });
}, { threshold: 0.2 });

document.querySelectorAll(".daftar li, .hasil pre").forEach(el => observer.observe(el));
