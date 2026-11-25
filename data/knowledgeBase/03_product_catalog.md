# Product Catalog — Reference Snapshot

> Fictional catalog for RAG testing. Prices are illustrative static reference values and are not live quotes. Inventory and current sale prices must be retrieved from an authorized commerce integration.

## Catalog rules

- Each SKU below identifies one reference product. Use the SKU when retrieving specifications, troubleshooting and warranty coverage.
- Prices are in USD and represent the standard list price before taxes, shipping and any eligible promotion.
- Product warranty durations are measured from delivery date. See `10_warranty_policy.md` for coverage and claim requirements.
- Bundle contents are included in the product descriptions/specifications where relevant. Marketplace listings may have a different SKU or bundle; verify the customer's purchase channel and SKU before applying this catalog.

## Active reference products

| SKU | Product name | Category | List price | Limited warranty | Description |
|---|---|---|---:|---:|---|
| NV-HUB8 | NovaLink 8-Port USB-C Hub | Computer accessories | $49.99 | 1 year | An aluminum multiport adapter for compatible USB-C laptops and tablets. |
| NV-CH65 | NovaCharge 65W USB-C Charger | Power and charging | $34.99 | 1 year | A compact single-port wall charger for USB-C Power Delivery devices. |
| NV-CAB100 | NovaFlex 100W USB-C Cable (2 m) | Cables | $17.99 | 1 year | A braided USB-C to USB-C cable for charging and data transfer. |
| NV-MSE2 | NovaGlide Bluetooth Mouse | Computer accessories | $29.99 | 1 year | A quiet wireless mouse for laptops and desktops. |
| NV-KB87 | NovaType 87 Mechanical Keyboard | Computer accessories | $79.99 | 1 year | A tenkeyless mechanical keyboard with hot-swappable switches. |
| NV-AUD1 | NovaSound ANC Wireless Headphones | Audio | $89.99 | 1 year | Over-ear Bluetooth headphones with active noise cancellation. |
| NV-SPK20 | NovaSound Go Bluetooth Speaker | Audio | $59.99 | 1 year | A portable splash-resistant speaker for indoor and outdoor listening. |
| NV-CAM1080 | NovaView 1080p USB Webcam | Cameras and streaming | $49.99 | 1 year | A plug-and-play webcam for video meetings and streaming. |
| NV-CAM4K | NovaView 4K Autofocus Webcam | Cameras and streaming | $99.99 | 1 year | A high-resolution autofocus webcam for compatible USB hosts. |
| NV-WC15 | NovaCharge 15W Qi Wireless Charging Stand | Power and charging | $39.99 | 1 year | A desktop wireless charging stand for supported Qi phones and earbuds. |
| NV-SP2 | NovaHome Smart Plug Mini (2-Pack) | Smart home | $24.99 | 1 year | Two app-controlled Wi-Fi plugs for scheduled control of household devices. |
| NV-BULB2 | NovaHome Matter Smart Bulbs A19 (2-Pack) | Smart home | $29.99 | 1 year | Two tunable-white Matter smart bulbs for connected homes. |
| NV-CAMIN | NovaHome Indoor Security Camera | Smart home | $59.99 | 1 year | A 2K indoor Wi-Fi camera with local microSD recording support. |
| NV-RTAX | NovaRoute AX1800 Wi-Fi 6 Router | Networking | $129.99 | 2 years | A dual-band Wi-Fi 6 router for home networks; modem is not included. |
| NV-SSD1T | NovaVault Portable SSD 1TB | Storage | $109.99 | 3 years | A compact external solid-state drive for file storage and backups. |
| NV-PB20 | NovaCharge 20K Power Bank | Power and charging | $49.99 | 1 year | A 20,000 mAh portable battery with USB-C Power Delivery output. |

## Product selection guidance

| Customer need | Products to consider | Qualification question |
|---|---|---|
| Add ports to a USB-C laptop | NV-HUB8 | Does the laptop's USB-C port support DisplayPort Alt Mode and USB PD? |
| Charge a USB-C laptop or tablet | NV-CH65 | What wattage does the device require? |
| Replace a charging cable | NV-CAB100 | Is USB 2.0 data sufficient, or is video/high-speed data needed? |
| Everyday wireless pointing | NV-MSE2 | Does the computer have Bluetooth? |
| Wired mechanical typing | NV-KB87 | Is an ANSI 87-key layout acceptable? |
| Noise reduction while listening | NV-AUD1 | Is Bluetooth or 3.5 mm wired use preferred? |
| Portable room audio | NV-SPK20 | Is IPX5 splash resistance sufficient (not submersion)? |
| Video meetings | NV-CAM1080 or NV-CAM4K | Does the host support USB 3.x if 4K is required? |
| Wireless phone charging | NV-WC15 | Does the phone support Qi, and what charging rate does it accept? |
| App-controlled outlet | NV-SP2 | Is 2.4 GHz Wi-Fi available, and is the appliance within the electrical rating? |
| Tunable-white smart lighting | NV-BULB2 | Is a Matter controller/ecosystem available? |
| Indoor monitoring | NV-CAMIN | Is 2.4 GHz Wi-Fi available, and is indoor-only use suitable? |
| Upgrade home wireless network | NV-RTAX | Is an existing modem/ONT or Ethernet handoff available? |
| Backups and portable storage | NV-SSD1T | Does the host have USB 3.x for peak speed? |
| Portable phone/tablet power | NV-PB20 | Is 20 W output enough for the device? |

## Dynamic product fields

The following cannot be answered from this static file: whether a product is currently in stock, exact ship date, a customer's negotiated price, an active coupon, an order-specific substitution or a marketplace-specific bundle. Use approved commerce tools or escalate. Never treat an old catalog snapshot as proof of present availability.

## Related documents

See `04_product_specifications.md`, `05_product_compatibility.md`, `10_warranty_policy.md` and `14_technical_troubleshooting.md`.
