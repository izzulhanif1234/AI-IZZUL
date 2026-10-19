/* PM Multilink — skrip halaman */

/* Kemaskini maklumat ini. WhatsApp: format antarabangsa tanpa "+" atau sengkang, contoh "60123456789". */
const SYARIKAT = {
  whatsapp: "",
  emel: "",
};

(function () {
  const pautanWa = (teks) =>
    SYARIKAT.whatsapp
      ? "https://wa.me/" + SYARIKAT.whatsapp + (teks ? "?text=" + encodeURIComponent(teks) : "")
      : "hubungi.html#borang";

  // Semua pautan WhatsApp ([data-wa]) ikut nombor dalam SYARIKAT
  document.querySelectorAll("[data-wa]").forEach((a) => {
    a.href = pautanWa(a.dataset.wa || "Salam, saya ingin bertanya tentang perkhidmatan PM Multilink.");
    if (SYARIKAT.whatsapp) { a.target = "_blank"; a.rel = "noopener"; }
  });

  // Menu mudah alih
  const togol = document.querySelector(".togol-menu");
  const menu = document.getElementById("menu-utama");
  if (togol && menu) {
    togol.addEventListener("click", () => {
      const buka = menu.classList.toggle("buka");
      togol.setAttribute("aria-expanded", String(buka));
    });
  }

  // Tahun semasa di pengaki
  document.querySelectorAll("[data-tahun]").forEach((el) => (el.textContent = new Date().getFullYear()));

  // Penapis galeri projek
  const butangPenapis = document.querySelectorAll(".penapis button");
  butangPenapis.forEach((b) => {
    b.addEventListener("click", () => {
      butangPenapis.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      const k = b.dataset.kategori;
      document.querySelectorAll(".projek").forEach((p) => {
        p.hidden = k !== "semua" && p.dataset.kategori !== k;
      });
    });
  });

  // Pilih perkhidmatan dalam borang daripada ?servis=... di URL
  const borang = document.getElementById("borang");
  if (borang) {
    const servis = new URLSearchParams(location.search).get("servis");
    if (servis && borang.servis.querySelector('option[value="' + servis + '"]')) borang.servis.value = servis;

    borang.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!borang.reportValidity()) return;
      const d = new FormData(borang);
      const mesej = [
        "Salam PM Multilink, saya ingin mendapatkan sebut harga.",
        "",
        "Nama: " + d.get("nama"),
        "Telefon: " + d.get("telefon"),
        "Perkhidmatan: " + borang.servis.options[borang.servis.selectedIndex].text,
        "Lokasi: " + (d.get("lokasi") || "-"),
        "",
        d.get("mesej"),
      ].join("\n");
      const status = document.getElementById("status-borang");

      if (SYARIKAT.whatsapp) {
        window.open(pautanWa(mesej), "_blank", "noopener");
        status.textContent = "WhatsApp dibuka dengan mesej anda. Tekan hantar untuk menghubungi kami.";
      } else if (SYARIKAT.emel) {
        location.href = "mailto:" + SYARIKAT.emel + "?subject=" + encodeURIComponent("Permintaan sebut harga") + "&body=" + encodeURIComponent(mesej);
        status.textContent = "Aplikasi emel anda dibuka dengan mesej ini.";
      } else {
        status.textContent = "Maaf, saluran hubungan belum ditetapkan. Sila hubungi kami melalui telefon.";
      }
    });
  }
})();
