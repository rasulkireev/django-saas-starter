import { Controller } from "@hotwired/stimulus";

import { copyText } from "../utils/clipboard";

export default class extends Controller {
  static targets = ["source", "label"];

  async copy() {
    const text = this.sourceTarget.value || this.sourceTarget.textContent || "";
    const copied = await copyText(text);
    const original = this.hasLabelTarget ? this.labelTarget.textContent : null;

    if (this.hasLabelTarget) {
      this.labelTarget.textContent = copied ? "Copied" : "Copy failed";
      window.clearTimeout(Number(this.labelTarget.dataset.resetTimer));
      this.labelTarget.dataset.resetTimer = window.setTimeout(() => {
        this.labelTarget.textContent = original;
      }, 1600);
    }
  }
}
