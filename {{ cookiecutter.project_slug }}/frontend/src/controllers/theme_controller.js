import { Controller } from "@hotwired/stimulus";

const STORAGE_KEY = "theme";

function preferredTheme() {
  if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    return "dark";
  }
  return "light";
}

function currentTheme() {
  return localStorage.getItem(STORAGE_KEY) || preferredTheme();
}

function applyTheme(theme) {
  const root = document.documentElement;
  if (theme === "dark") {
    root.classList.add("dark");
  } else {
    root.classList.remove("dark");
  }
}

export default class extends Controller {
  static targets = ["iconLight", "iconDark", "label"]; // all optional

  connect() {
    applyTheme(currentTheme());
    this.updateUI();
  }

  toggle() {
    const next = currentTheme() === "dark" ? "light" : "dark";
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
    this.updateUI();
  }

  updateUI() {
    const theme = currentTheme();

    if (this.hasIconLightTarget) this.iconLightTarget.classList.toggle("hidden", theme !== "light");
    if (this.hasIconDarkTarget) this.iconDarkTarget.classList.toggle("hidden", theme !== "dark");

    if (this.hasLabelTarget) {
      this.labelTarget.textContent = theme === "dark" ? "Dark" : "Light";
    }

    this.element.setAttribute(
      "aria-label",
      theme === "dark" ? "Switch to light mode" : "Switch to dark mode",
    );
  }
}
