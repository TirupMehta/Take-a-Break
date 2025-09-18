# Break Reminder App

A **minimal, distraction-proof break reminder application** built with **Python (PyQt5)**.
This app ensures you take regular breaks by showing a **full-screen overlay** every hour that cannot be skipped until the timer completes.

Perfect for anyone looking to reduce eye strain, improve focus, and maintain healthy work habits.

---

## 📥 Download the App

👉 [**Click here to download the latest version**](../../releases)

You can use the app in **two ways**:

### 1. Direct App (No Python Required)

* Download the `.exe` file from the [Releases](../../releases) page.
* Run it directly on Windows — no installation or setup needed.
* The app will start minimized in your **system tray**.

### 2. Run from Source (Python)

If you prefer to run or modify the code:

#### Requirements

* Python **3.8+**
* Dependencies:

  ```bash
  pip install PyQt5
  ```

#### Run

```bash
python break_reminder.py
```

---

## ✨ Features

* **Full-Screen Break Overlay** – Covers the screen with a clean, dark UI.
* **2-Minute Timer** – Encourages short, effective breaks.
* **Snooze (Max 3 per day)** – Postpone a break for 1 hour if needed.
* **System Tray Integration** – Quick access to “Show Break Now” or “Exit App.”
* **Cross-Platform** – `.exe` for Windows, source code works on Linux/macOS too.
* **Lightweight & Minimal** – Focused only on essential functionality.

---

## 🚀 Usage

1. Launch the app (via `.exe` or Python script).
2. It runs silently in the **system tray**.
3. A **test break** will trigger after 2 minutes (to confirm setup).
4. After that, a **break overlay appears every hour**.
5. During a break:

   * Wait for the **2-minute timer** to finish.
   * Or use **Snooze (1 hour)** if you still need time (limited to 3/day).
   * Once the timer ends, you can **quit the break screen** and continue work.

---

## ⚙️ Configuration

* **Break Interval** – Default: 1 hour.
* **Break Duration** – Default: 2 minutes.
* **Daily Snooze Limit** – 3 times/day.
* State is tracked in:

  ```
  ~/.break_reminder_state.json
  ```


---

## 🔨 Build Instructions (For Developers)

If you want to generate your own `.exe` file:

1. Install **PyInstaller**:

   ```bash
   pip install pyinstaller
   ```
2. Build:

   ```bash
   pyinstaller --onefile --noconsole break_reminder.py
   ```
3. The `.exe` will be available in the `dist/` folder.

---

## 🧑‍💻 Contributing

Contributions, feature requests, and issues are welcome!
Please open a GitHub **issue** or **pull request** if you’d like to improve the app.

---

## 📜 License

MIT License © 2025 [Tirup Mehta](https://github.com/TirupMehta)

You’re free to use, modify, and distribute this project with proper attribution.
