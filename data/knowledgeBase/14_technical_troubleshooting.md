# Technical Troubleshooting Playbook

## Safety before troubleshooting

Do not continue testing a product that is smoking, sparking, swollen, leaking, emitting a burning/chemical odor, unusually hot or causing an electrical shock. Tell the customer to stop using it, disconnect power only if it is safe to do so, keep it away from combustible materials and route the case immediately to Product Safety/Product Support. Do not advise opening sealed electronics, puncturing batteries or attempting component-level repair.

The steps below are limited to non-invasive checks. Ask the customer to change one variable at a time and report the observed result. Do not require the customer to share passwords, verification codes or private account credentials.

## NV-HUB8 — HDMI display not detected

**Diagnostic steps:** Confirm the laptop USB-C port supports DisplayPort Alt Mode; connect the hub directly to the host; select the correct monitor input; reseat the HDMI cable; test another display/cable; disconnect other peripherals to check power load. The hub cannot add video capability to a USB-C port without Alt Mode.

**Human-support threshold:** If the host specification confirms Alt Mode and the issue persists with a known-good display/cable, route to Product Support. Do not instruct opening the hub.

## NV-CH65 — Device charges slowly

**Diagnostic steps:** Check the device's required wattage; use a USB-C PD-compatible cable; connect directly to the charger; remove high-load apps temporarily; test another supported PD device. The output is capped at 65 W and negotiated by the host.

**Human-support threshold:** Escalate if the charger becomes abnormally hot, smells burnt, sparks or repeatedly disconnects. Stop using it in safety cases.

## NV-CAB100 — File transfer is slow

**Diagnostic steps:** Explain that this cable supports USB 2.0 data up to 480 Mbps, not USB 3.x/Thunderbolt. Test with a small file and confirm the device/port. Use a high-speed cable if the customer's task requires faster data or video.

**Human-support threshold:** Usually a capability clarification, not a defect. Escalate only if charging/data connection is intermittent on multiple known-good hosts.

## NV-MSE2 — Mouse will not pair

**Diagnostic steps:** Replace/check the AA battery; turn the mouse off and on; enable Bluetooth on the host; remove an old pairing entry; place the mouse in pairing mode per the quick-start guide; scan again. Confirm the host supports Bluetooth.

**Human-support threshold:** If it fails to appear on two compatible hosts with a fresh battery, create a Product Support case.

## NV-KB87 — Keyboard keys do not respond

**Diagnostic steps:** Disconnect and reconnect the USB cable; try a different direct USB port; avoid an unpowered hub during diagnosis; verify the correct keyboard layout in the OS; test in a text field. Confirm the USB-C cable is fully seated.

**Human-support threshold:** Escalate if keys remain unresponsive on two computers or there is liquid/impact damage. Do not recommend opening the keyboard.

## NV-AUD1 — Headphones will not connect

**Diagnostic steps:** Charge the headset; remove stale Bluetooth pairing on the host; place headphones in pairing mode; keep them near the host; disconnect from another paired device; test wired 3.5 mm mode to isolate Bluetooth audio.

**Human-support threshold:** Escalate after failure on two compatible hosts, or immediately for battery swelling, unusual heat or burning odor. Stop use for safety symptoms.

## NV-SPK20 — Speaker will not charge

**Diagnostic steps:** Use a known-good USB-C 5 V/2 A source and cable; inspect the port for visible debris without inserting metal tools; allow a short cool-down if warm; check the charge indicator. Do not charge while wet.

**Human-support threshold:** Stop use if it swells, smokes, smells burnt or becomes unusually hot. Otherwise escalate if no indicator appears with a known-good cable/source.

## NV-CAM1080 — Webcam unavailable in meeting app

**Diagnostic steps:** Reconnect USB; select NovaView 1080p in the app's camera list; grant OS camera/microphone permissions; close another app that may be using the camera; test in a second supported app; avoid an unpowered hub.

**Human-support threshold:** Escalate if not detected on two supported computers after permission and cable checks.

## NV-CAM4K — 4K mode unavailable

**Diagnostic steps:** Check the host port is USB 3.x; connect directly or through a verified USB 3.x hub; select 4K in camera/app settings; close bandwidth-heavy USB devices; verify the conferencing service supports 4K. Many services cap resolution.

**Human-support threshold:** Escalate if 4K is unavailable on a confirmed USB 3.x host and an app that supports 4K, after checking settings.

## NV-WC15 — Wireless charging starts and stops

**Diagnostic steps:** Center the phone's charging coil on the stand; remove metal plates, magnetic accessories or thick cases; use a suitable 9 V/2 A USB-C power source; let the device cool; confirm Qi support. A lower wattage may be normal for the phone.

**Human-support threshold:** Escalate for persistent failure on two Qi devices with a suitable adapter, or immediately for overheating/burning odor.

## NV-SP2 — Smart plug will not pair

**Diagnostic steps:** Confirm the phone and plug are on a 2.4 GHz Wi-Fi network; enable Bluetooth/location permissions if the app setup requires them; move near the router; power-cycle the plug; verify the router is not 5 GHz-only or using an unsupported isolation setting.

**Human-support threshold:** Escalate if it cannot pair after router-band confirmation and reset steps. For overload, hot outlet or sparking, unplug safely if possible and escalate immediately.

## NV-BULB2 — Smart bulb appears offline

**Diagnostic steps:** Confirm the wall switch is on; verify 2.4 GHz Wi-Fi; confirm the Matter controller is online; check whether the bulb was removed from another ecosystem; power-cycle once. Do not use with a traditional dimmer.

**Human-support threshold:** Escalate if commissioning fails with a compatible Matter controller and supported Wi-Fi. If the bulb flickers on a dimmer, switch off and stop using that dimmer combination.

## NV-CAMIN — Camera cannot connect remotely

**Diagnostic steps:** Confirm camera power; check 2.4 GHz Wi-Fi and internet access; restart the router/camera; verify the app account is signed in; check whether local network permissions are granted. For microSD, confirm supported capacity up to 128 GB and format/configure it in the app.

**Human-support threshold:** Escalate after network checks if the camera remains offline. Suspected unauthorized viewing/account access goes to Trust & Safety immediately.

## NV-RTAX — No internet after installation

**Diagnostic steps:** Confirm the ISP modem/ONT is online; connect its Ethernet output to the router WAN port; restart modem first, then router; check WAN cable and ISP credentials/settings; test a wired LAN device. Remember the router is not a modem.

**Human-support threshold:** If the modem/ONT has no provider signal, direct the customer to the ISP. Escalate router hardware faults after a known-good Ethernet handoff and cable are confirmed.

## NV-SSD1T — Drive not visible

**Diagnostic steps:** Try a different USB port and supplied cable; connect directly; check Disk Management/Disk Utility without initializing or formatting; test another computer; confirm the port supports USB storage. Back up data before any format operation.

**Human-support threshold:** If the drive contains inaccessible important data, do not advise formatting or recovery utilities that may overwrite it; escalate to Storage Support. Physical damage or unusual heat requires stop-use guidance.

## NV-PB20 — Power bank output stops

**Diagnostic steps:** Recharge the bank; use a compatible cable; press the power/status button if required; disconnect all ports and reconnect one device; confirm device demand does not exceed 20 W USB-C output. Multiple-port use shares power and lowers available output.

**Human-support threshold:** Stop using and escalate immediately for swelling, leakage, smoke, burning odor or abnormal heat. For normal underpowered laptop use, explain the 20 W limit.

## Troubleshooting record fields

When opening a support ticket, capture only what is necessary: product SKU/model, purchase channel, order reference after verification, host/device model, operating-system version where relevant, symptom, when it began, steps already attempted, error text, and whether there are safety symptoms. Photos/logs should be submitted only through an approved secure upload mechanism.

## Static versus live troubleshooting

This playbook is static. A customer's warranty eligibility, replacement stock, firmware availability, order status and case history are dynamic and require authorized system lookup. Never invent a diagnostic result or claim that a firmware update exists unless the current approved support system confirms it.
