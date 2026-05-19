import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["modal", "confirmation", "submit"]; // submit optional

  open() {
    if (!this.hasModalTarget) return;
    this.modalTarget.classList.remove("hidden");
    this.modalTarget.classList.add("flex");

    if (this.hasConfirmationTarget) {
      this.confirmationTarget.value = "";
      this.confirmationTarget.focus();
    }

    this.update();
  }

  close() {
    if (!this.hasModalTarget) return;
    this.modalTarget.classList.add("hidden");
    this.modalTarget.classList.remove("flex");
  }

  update() {
    if (!this.hasSubmitTarget || !this.hasConfirmationTarget) return;
    this.submitTarget.disabled = this.confirmationTarget.value !== "DELETE";
  }
}
