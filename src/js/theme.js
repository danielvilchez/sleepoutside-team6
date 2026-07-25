const storageKey = "so-theme";

function getTheme() {
  const savedTheme = localStorage.getItem(storageKey);

  if (savedTheme) {
    return savedTheme;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function applyTheme(theme, button) {
  document.documentElement.dataset.theme = theme;

  if (button) {
    const nextTheme = theme === "dark" ? "light" : "dark";
    button.textContent = nextTheme === "dark" ? "Dark mode" : "Light mode";
    button.setAttribute("aria-label", `Activate ${nextTheme} mode`);
  }
}

function setupTheme() {
  const header = document.querySelector("header");

  if (!header) {
    return;
  }

  const button = document.createElement("button");
  button.className = "theme-toggle";
  button.type = "button";

  header.insertBefore(button, header.querySelector(".cart"));

  let currentTheme = getTheme();
  applyTheme(currentTheme, button);

  button.addEventListener("click", () => {
    currentTheme = currentTheme === "dark" ? "light" : "dark";
    localStorage.setItem(storageKey, currentTheme);
    applyTheme(currentTheme, button);
  });
}

setupTheme();
