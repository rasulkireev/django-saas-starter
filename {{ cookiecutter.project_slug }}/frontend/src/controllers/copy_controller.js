import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["source", "label"];

  async copy() {
    const text = this.sourceTarget.value || this.sourceTarget.textContent || "";
    const copied = await this.copyText(text);
    const original = this.hasLabelTarget ? this.labelTarget.textContent : null;

    if (this.hasLabelTarget) {
      this.labelTarget.textContent = copied ? "Copied" : "Copy failed";
      window.clearTimeout(Number(this.labelTarget.dataset.resetTimer));
      this.labelTarget.dataset.resetTimer = window.setTimeout(() => {
        this.labelTarget.textContent = original;
      }, 1600);
    }
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
