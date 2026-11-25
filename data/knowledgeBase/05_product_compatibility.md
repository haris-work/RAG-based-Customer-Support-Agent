# Product Compatibility Guide

## General compatibility rules

Compatibility depends on both the NovaTech product and the customer's host device, operating system, port implementation, network and configuration. The presence of a connector with a familiar shape does not prove that every protocol is supported.

## USB-C, USB Power Delivery and video

- USB-C describes a connector shape; it does not automatically mean USB 3.x data, video output, Thunderbolt or high-wattage charging.
- **NV-HUB8:** Basic USB data functions require a compatible USB-C host. HDMI output requires DisplayPort Alt Mode. Power passthrough requires a USB PD source and compatible host. A USB-C port without video Alt Mode will not produce HDMI video through the hub.
- **NV-CH65:** Supplies up to 65 W using USB PD 3.0/PPS negotiation. A laptop rated for 90 W may charge slowly or may not maintain charge during heavy use. Device and cable determine the negotiated rate.
- **NV-CAB100:** Supports up to 100 W USB PD charging and USB 2.0 data at up to 480 Mbps. It does not support DisplayPort video, Thunderbolt or USB 3.x transfer speeds.
- **NV-SSD1T:** Peak throughput requires a USB 3.2 Gen 2 (10 Gbps) host and compatible cable/port. Slower ports work at their own limits.
- **NV-CAM4K:** A USB 3.x connection is needed for its highest-resolution modes. A USB 2.0 connection may reduce resolution/frame rate or prevent stable operation.

## Bluetooth products

- **NV-MSE2** uses Bluetooth 5.1 and requires a host with Bluetooth input-device support. It has no included USB receiver and cannot connect as a wired mouse.
- **NV-AUD1** and **NV-SPK20** use standard Bluetooth audio profiles. The host must support Bluetooth audio; microphone routing in calls is controlled by the operating system and conferencing app. Codec support such as AAC varies by host.
- Bluetooth version numbers are backward-compatible in many common cases, but the oldest device may limit available features. Do not promise a precise range; walls, interference and radio design affect it.

## Wireless charging

- **NV-WC15** requires a Qi-compatible receiving device. Its 15 W maximum is not available to every phone. Some phone families negotiate a lower rate. Thick cases, metal plates, magnets or poor coil alignment may stop or slow charging.
- The NV-WC15 is not represented as MagSafe-certified. Do not promise magnetic attachment or a specific iPhone charging rate.

## Smart-home Wi-Fi, Matter and electrical limits

- **NV-SP2** and **NV-CAMIN** require a 2.4 GHz Wi-Fi network. A combined 2.4/5 GHz network may work when the router permits 2.4 GHz client onboarding; a 5 GHz-only network will not.
- **NV-BULB2** uses Matter over Wi-Fi and requires a compatible Matter controller/ecosystem for the customer's chosen control method. Matter does not mean every feature is exposed identically in every app.
- **NV-SP2** is rated for up to 15 A resistive load / 1,800 W at 120 V. It is indoor-only and must not control medical/life-support equipment or loads exceeding the rating. Motor loads and high inrush can be unsuitable even if their nominal wattage appears low.
- **NV-BULB2** must not be used with a conventional wall dimmer. The wall switch must remain on for app control.
- **NV-CAMIN** is indoor-only. Remote access needs internet connectivity. Local recording needs a compatible microSD card and configured recording option.

## Router and internet compatibility

**NV-RTAX** is a Wi-Fi router, not a modem. It connects to an existing cable/DSL/fiber modem or an Ethernet handoff from the provider. It cannot directly terminate a coaxial cable, telephone DSL line or fiber optic line. The ISP may require bridge mode, PPPoE credentials or VLAN settings; if the customer does not know these values, direct them to the ISP rather than guessing.

## Operating-system guidance

- NV-MSE2: Windows 10/11, macOS 12+, ChromeOS and common Linux Bluetooth desktop stacks.
- NV-KB87: Standard USB keyboard input on Windows, macOS and Linux; some function shortcuts are platform-specific.
- NV-CAM1080 and NV-CAM4K: UVC support on current Windows/macOS/ChromeOS and most Linux distributions; app permissions must be granted.
- NV-SSD1T: USB mass-storage support; filesystem compatibility varies by device. It ships exFAT-formatted.

## When compatibility is uncertain

Ask for the exact host model, operating-system version, port type and intended use. Do not state “fully compatible” from connector shape alone. For an unlisted device combination, say it is not confirmed in this knowledge base and offer Product Support review.
