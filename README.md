# BaseOS-v90s

> [!IMPORTANT]
> **Provided As-Is:** `BaseOS-v90s` and [`NextUI-v90s`](https://github.com/Pobega/NextUI-v90s) are provided **as-is**. They are **not** intended to be fully maintained forks of [BaseOS](https://github.com/pvaibhav/BaseOS) or [NextUI](https://github.com/LoveRetro/NextUI), but rather a standalone port meant to give Powkiddy V90S users a fast, clean experience (~5.9s cold boot to menu). There may be bugs or missing features—feel free to report issues, though it is not extremely likely that all of them will be fixed.

`BaseOS-v90s` is a port of [BaseOS](https://github.com/pvaibhav/BaseOS) to the **Powkiddy V90S** (Allwinner A133P / `sun50iw10p1`), paired with [`NextUI-v90s`](https://github.com/Pobega/NextUI-v90s). It replaces the slow Batocera/PlumOS-based stock userland (~25+ second boot) with a minimal BusyBox-based system that boots straight into NextUI in under 6 seconds.

## Powkiddy V90S Quick Start (`BaseOS-v90s` + `NextUI-v90s`)

1. **Flash `BaseOS-v90s` to TF1:**
   Download `baseos-v90s-<version>.img.zip` from the [`BaseOS-v90s` Releases page](https://github.com/Pobega/BaseOS-v90s/releases), extract `baseos-v90s-<version>.img`, and flash it to your **TF1** microSD card (using Raspberry Pi Imager, BalenaEtcher, or `dd`). **Do not reformat TF1 after flashing.**
2. **First Boot (Optional if using a Single SD Card):**
   Insert TF1 into your V90S and power it on once so `BaseOS-v90s` automatically expands the `BASEOS` data partition to fill the rest of your TF1 card, or mount the `BASEOS` partition directly on your computer.
3. **Add `NextUI-v90s` (Single-Card or Dual-Card Setup):**
   Download `NextUI-*-v90s-*-base.zip` (or `-all.zip` to include extra emulators/tools) from the [`NextUI-v90s` Releases page](https://github.com/Pobega/NextUI-v90s/releases):
   - **Single SD Card (TF1 only):** Extract the contents of the `NextUI-*-v90s-*.zip` release (`MinUI.zip`, `*.pakz`, `Bios/`, `Roms/`, `Saves/`) onto the root of TF1's visible `BASEOS` partition. **Keep `MinUI.zip` and any `*.pakz` files zipped**—`BaseOS-v90s` extracts and installs them automatically on boot.
   - **Two SD Cards (TF1 + TF2):** Format a second microSD card (TF2) as **FAT32** or **exFAT** and extract the contents of the `NextUI-*-v90s-*.zip` release (`MinUI.zip`, `*.pakz`, `Bios/`, `Roms/`, `Saves/`) to the root of TF2. When both cards are inserted, TF2 takes priority over TF1.
4. **Boot & Play:**
   Insert your card(s) into the V90S and power on. On the first boot with `MinUI.zip` present, `BaseOS-v90s` displays **INSTALLING FRONTEND**, unpacks `NextUI-v90s`, and launches into the menu. Subsequent boots go straight to NextUI in ~5.9 seconds (`~3.6s` before Linux + `~2.3s` Linux to NextUI).

### Powkiddy V90S Hardware Notes

- **Supported on V90S:** 640×480 display, controls (`adc_gamepad`), speaker audio (`sun50iw10codec`), volume and brightness shortcuts, rumble/vibration, deep sleep / power off, USB `adb`, writable USB storage mode (hold **MENU** while powering on with USB-C connected), optional `startup_sound.wav` on TF1, and single-file `.bosupd` A/B system updates.
- **V90S Hardware Limitations:** Unlike Anbernic H700 handhelds, the Powkiddy V90S hardware does not include built-in Wi-Fi, Bluetooth, HDMI output, or a magnetic lid/Hall sensor (putting the device to sleep is done via a short press of the **POWER** button).

---

## Upstream BaseOS Documentation (Anbernic RG XX & V90S)

BaseOS is a small, fast operating system for Anbernic RG XX handhelds (and ported here to the Powkiddy V90S). It
handles the hardware and starts your choice of frontend:
[NextUI](https://nextui.loveretro.games), [Slot](https://slot-cfw.fyi),
[spruceOS](https://spruceui.github.io), or your own. It has no menu of its own.

**[Upstream Installation guide](https://github.com/pvaibhav/BaseOS/wiki/BaseOS-Install-Guide)**

## Startup time

![Total BaseOS startup time across releases, from about 6.7 seconds to 3.16 seconds](assets/boot-times.svg)

These times include kernel loading but not frontend loading.

v1.4.0 also loads NextUI about 0.7 seconds faster and Slot about 0.3 seconds
faster.

## Features

- Display, sound, controls, Wi-Fi, HDMI, LEDs and deep sleep support.
- A small system with minimal background activity.
- Automatic expansion to use the full SD card on first boot.
- Updates by copying one file to your card. Games, saves and settings stay put.
- SSH/SFTP over Wi-Fi and adb over USB, enabled by default.
- USB storage mode to access your card from a computer.
- Optional startup sound: put `startup_sound.wav` at the root of TF1's BASEOS
  partition. Use a short WAV clip; other formats are not supported.

## Installation and updates

For a fresh install, [download your model's BaseOS release](https://github.com/pvaibhav/BaseOS/releases/latest),
unzip its `.img.zip` and flash the `.img` to TF1. Flashing erases the card.
Then add a frontend using TF1's visible `BASEOS` volume or a separate TF2 card.
**Do not reformat TF1 after flashing BaseOS.** A usable TF2 card takes priority.

Use one frontend per card. FAT32 works with all three frontends; NextUI also
supports exFAT on TF2. Follow the
[installation guide](https://github.com/pvaibhav/BaseOS/wiki/BaseOS-Install-Guide)
for one-card or two-card setup.

To update BaseOS, copy your model's `.bosupd` to the root of your frontend card
and restart. Keep power connected during the v1.4.0 update's one-time startup
optimisation, and let it finish without switching off. From v1.5.2, the new
boot method installs at any battery level. It takes a few seconds on the first
start after the update, while the screen shows "SPEEDING UP BOOT".

If startup looks wrong, check `baseos-boot.log` at the root of the card. It
says which startup ran and why.

### Frontends

- **NextUI:** [official v6.15.0 and later](https://github.com/LoveRetro/NextUI/releases/latest)
  support H700 natively. Extract the `-base.zip` or `-all.zip` archive and copy
  its contents to your frontend card's root. Keep `MinUI.zip` zipped. BaseOS
  installs it automatically. You don't need a separate H700 fork or the
  stock-OS `dmenu.bin` setup. [NextUI installation guide](https://nextui.loveretro.games/getting-started/installation/).
- **Slot:** extract its [H700 release](https://github.com/BrandonKowalski/slot/releases/latest)
  and copy the contents of `slot-<version>` to the card root, including the
  complete `System/` folder. Put unzipped games in `Games/GB/`, `Games/GBC/`
  or `Games/GBA/`, and optional BIOS files in `BIOS/`. Update by replacing
  `System/` with the folder from the new release. [Slot guide](https://slot-cfw.fyi).
  For RetroAchievements, cheats and a few extra goodies, try
  [my Slot fork](https://github.com/pvaibhav/slot).
- **spruceOS:** extract the full [release archive](https://github.com/spruceUI/spruceOS/releases/latest)
  and copy all contents, including hidden folders, to the card root. The card
  should then contain `spruce/scripts/runtime.sh`. The
  [spruceOS Installer](https://github.com/spruceUI/spruceOS-Installer/releases/latest)
  can set up a separate TF2 card; skip its TF1 image step if BaseOS is already
  installed. [spruceOS installation guide](https://github.com/spruceUI/spruceOS/wiki/01.-Installation-Instructions).
- **Your own frontend:** add `System/launch_frontend.sh` or a glibc AArch64
  binary at `System/frontend`. The binary takes priority. Scripts run through
  `/bin/sh`. Both run from the card root and need no executable bit.

## Settings

Edit `baseos.conf` at the root of TF1's visible partition, then restart.
Settings stay on TF1 even when your frontend is on TF2, and they survive OS
updates.

```ini
hostname=my-handheld
mdns=true
```

- **`hostname`**: your device's network name. Defaults to its model ID, such as
  `rg34xxsp`. Use 1–63 letters, digits or hyphens, with no hyphen at either end.
- **`mdns`**: connect using `<hostname>.local` over Wi-Fi. Enabled by default.
  Set `false` to disable it.
- **`ssh_password`**: set your SSH password. Defaults to `root` if omitted or
  empty. `baseos.conf` holds it as plain text, so don't reuse an
  important password. Write it without quotes. BaseOS trims surrounding spaces.
- **`headphone_pop_fix`**: set `true` to try the headphone exit-pop fix. It is
  off by default because it can use more battery while awake. The speaker pop fix is
  always enabled. See [audio support](docs/05-runtime-power-network.md#speaker-and-headphone-pop-repair).

Omitted settings use their defaults. Lines starting with `#` are comments, but
a `#` within an SSH password is part of the password.

## USB access

For adb, connect a data-capable USB-C cable before powering on. If adb stops
working after unplugging it, restart with the cable connected.

For USB storage, hold **MENU** while connecting the cable. If the handheld
doesn't start automatically, hold Power for 3–4 seconds. Release Power when it
starts, but keep holding MENU until you see **"USB STORAGE: EJECT BEFORE
RESTART"**.

Eject the drive on your computer before restarting the handheld. Restart
without holding MENU to return to normal.

## Supported devices

- **Powkiddy V90S** (`v90s` — Allwinner A133P)
- Anbernic RG28XX
- Anbernic RG34XX
- Anbernic RG34XX SP
- Anbernic RG35XX Plus and RG35XX 2024
- Anbernic RG35XX H
- Anbernic RG35XX Pro
- Anbernic RG35XX SP
- Anbernic RG40XX H
- Anbernic RG40XX V
- Anbernic RG CubeXX
- Anbernic RG SP

## How it works

BaseOS uses the vendor's bootloader, kernel and hardware drivers (Allwinner
A133P for the Powkiddy V90S; Allwinner H700 for Anbernic RG XX handhelds), with
a minimal BusyBox-based system in place of the stock userland. From version
1.3.0, BaseOS stores the kernel in compressed form to reduce loading work. The
kernel itself is unchanged.

Build instructions and technical documentation are in
[CONTRIBUTING.md](CONTRIBUTING.md).
