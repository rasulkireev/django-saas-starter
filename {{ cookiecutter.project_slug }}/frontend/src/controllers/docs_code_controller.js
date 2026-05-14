import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  connect() {
    this.addCopyButtons();
  }

  addCopyButtons() {
    const blocks = this.element.querySelectorAll("pre");

    blocks.forEach((block) => {
      if (block.dataset.copyEnhanced === "true") {
        return;
      }

      const code = block.querySelector("code");
      if (!code) {
        return;
      }

      block.dataset.copyEnhanced = "true";
      const wrapper = document.createElement("div");
      wrapper.className = "group relative my-6";
      block.parentNode.insertBefore(wrapper, block);
      wrapper.appendChild(block);

      const button = document.createElement("button");
      button.type = "button";
      button.className = "absolute right-3 top-3 rounded-lg border border-gray-700 bg-gray-900/90 px-2.5 py-1 text-xs font-semibold text-gray-200 opacity-0 shadow-sm transition hover:bg-gray-800 focus:opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-{{ cookiecutter.project_main_color }}-500 group-hover:opacity-100";
      button.textContent = "Copy";
      button.addEventListener("click", () => this.copyCode(code.textContent, button));
      wrapper.appendChild(button);
    });
  }

  async copyCode(text, button) {
    const copied = await this.copyText(text);
    const original = button.dataset.originalLabel || button.textContent;
    button.dataset.originalLabel = original;
    button.textContent = copied ? "Copied" : "Copy failed";
    window.clearTimeout(Number(button.dataset.resetTimer));
    button.dataset.resetTimer = window.setTimeout(() => {
      button.textContent = original;
    }, 1600);
  }

  async copyText(text) {
    if (navigator.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (error) {
        // Fall back for restricted clipboard contexts.
      }
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.top = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();

    try {
      return document.execCommand("copy");
    } catch (error) {
      return false;
    } finally {
      textarea.remove();
    }
  }
}
