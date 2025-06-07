import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  connect() {
    this.fetchAndStoreSettings();
  }

  async fetchAndStoreSettings() {
    try {
      const response = await fetch(`/api/user/settings`);
      if (!response.ok) {
        // This is a background task, so just log errors, don't alert the user.
        console.error("Failed to fetch user settings in the background.");
        return;
      }
      const data = await response.json();

      localStorage.setItem(`userSettings`, JSON.stringify(data));

    } catch (error) {
      console.error("Error fetching user settings:", error);
    }
  }
}
