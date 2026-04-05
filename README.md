# HP Brightness Control via Fn Keys

Control display brightness using **Fn+F3** (decrease) and **Fn+F4** (increase) on supported HP devices.

## ✅ Tested Devices

- **HP Victus Laptop**
- **HP E23 G4 Monitor**

## 📋 Requirements

- Windows 10 or later
- HP hotkey support enabled in BIOS/UEFI
- Administrator privileges for installation

## 🚀 Installation

### From Releases (Recommended)

1. Navigate to the [Releases](../../releases) page
2. Download the latest `.exe` or `.msi` installer
3. Run the installer with administrator privileges
4. Restart your system

> **Note:** Not all files are committed to `main`. Always download from [Releases](../../releases) for the complete, tested package.

### Manual Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hp-brightness-control.git
   cd hp-brightness-control
   ```

2. Run the setup script:
   ```bash
   python setup.py install
   ```

## 🎮 Usage

Once installed, simply press:

- **Fn + F3** — Decrease brightness
- **Fn + F4** — Increase brightness

Brightness adjusts in 10% increments. Confirmation via OSD (On-Screen Display) may appear depending on your device.

## ⚙️ Configuration

Edit `config.ini` to customize behavior:

```ini
[brightness]
step_size = 10           ; Brightness increment/decrement (1-100)
display_osd = true       ; Show on-screen display notification
min_brightness = 10      ; Minimum brightness level (%)
max_brightness = 100     ; Maximum brightness level (%)
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Keys don't respond | Ensure HP hotkey drivers are installed; check Device Manager for missing drivers |
| Brightness won't change below 10% | Adjust `min_brightness` in `config.ini` |
| Service won't start | Run installer as administrator; check Windows Event Viewer for errors |
| Conflicts with other tools | Disable OmenMon or similar performance tools temporarily |


## 🤝 Contributing

Found a bug or want to add support for another device?

1. Test on your device and document results
2. Open an issue with device model and OS version
3. Submit a pull request with improvements

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This tool modifies display settings at the system level. Use at your own risk. The authors are not responsible for any hardware damage or display anomalies resulting from improper use.

---

**Last Updated:** April 2026  
**Supported OS:** Windows 10, 11  
**Status:** Stable (v1.0)
