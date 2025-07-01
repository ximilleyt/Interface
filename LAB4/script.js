document.addEventListener("DOMContentLoaded", () => {
    const pages = document.querySelectorAll(".page");
    const navButtons = document.querySelectorAll(".sidebar-item");
    const themeSelect = document.querySelector(".theme-select");
    const saveBtn = document.querySelector(".btn.save");
    const resultTextAreas = document.querySelectorAll(".result-text");

    const applyTheme = (theme) => {
      document.body.classList.toggle("light-theme", theme === "light");
      document.body.classList.toggle("dark-theme", theme === "dark");
      themeSelect.value = theme;
    };
    const savedTheme = localStorage.getItem("theme") || "dark";
    applyTheme(savedTheme);
    saveBtn.addEventListener("click", () => {
      const selected = themeSelect.value;
      localStorage.setItem("theme", selected);
      applyTheme(selected);
    });
    navButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.dataset.tab;
        pages.forEach((page) => {
          page.classList.remove("active");
          if (page.id === targetId) page.classList.add("active");
        });
        navButtons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
      });
    });

    function showSkeleton(form) {
      form.querySelectorAll(".result-text").forEach(area => {
        area.value = "";
        area.classList.add("loading");
      });
    }
    function hideSkeletonWithResult(form, result) {
      form.querySelectorAll(".result-text").forEach(area => {
        area.classList.remove("loading");
        area.value = result;
      });
    }

    document.querySelectorAll("form.basic-form, form.advanced-form").forEach(form => {
      form.addEventListener("submit", e => {
        e.preventDefault();
        const action = e.submitter.value;
        const container = e.submitter.closest(".split-container");
        const textArea = action === 'encrypt'
          ? container.querySelector("textarea:not(.encrypted)")
          : container.querySelector("textarea.encrypted");
        const keyInput = container.querySelector(".input-key");

        if (!textArea.value.trim()) {
          alert(action === 'encrypt'
            ? "Пожалуйста, введите текст для шифрования."
            : "Пожалуйста, введите зашифрованный текст для дешифрования.");
          return;
        }
        if (action === 'decrypt' && keyInput && !keyInput.value.trim()) {
          alert("Пожалуйста, введите ключ для дешифрования.");
          return;
        }

        showSkeleton(form);
        setTimeout(() => {
          const dummy = action === 'encrypt'
            ? "Зашифрованный текст"
            : "Дешифрованный текст";
          hideSkeletonWithResult(form, dummy);
        }, 1500);
      });
    });

    navButtons[0].classList.add("active");
  });