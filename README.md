# Feather ESP32 V2 — Air Quality Monitor

CircuitPython 9.2.7 project for the Adafruit Feather ESP32 V2. Reads particulate matter, temperature, and humidity, posts data to Adafruit IO, and displays EPA AQI level on a NeoPixel strip. Includes a web dashboard hosted on GitHub Pages.

## Hardware

- Adafruit Feather ESP32 V2
- PM2.5 UART sensor (connected to TX/RX)
- AHT10/AHT20 temp+humidity sensor (I2C via STEMMA QT)
- 8-pixel NeoPixel strip (on D15)
- Potentiometer (on A4)
- LiPo battery charger with PGOOD on D13, CHARGE on D12

## NeoPixel Layout

The 8-pixel strip (index 0–7) is used as follows:

| Pixel | Index | Purpose |
|-------|-------|---------|
| Charger status | 0 | Red = charging, Green = full/power connected, Off = on battery |
| Network status | 1 | Blue = connected but not yet uploaded, Red = upload error, Off = uploading on tempo |
| AQI level | 2–7 | Rightmost pixels show EPA AQI level (see below) |

The AQI pixels fill from the right — the number of lit pixels and their color indicates the current EPA level based on the rolling PM2.5 average:

| Level | PM2.5 | Color | Pixels lit |
|-------|-------|-------|------------|
| Good | < 12.0 | Green | 1 |
| Moderate | < 35.0 | Yellow | 2 |
| Unhealthy for Sensitive Groups | < 55.0 | Orange | 3 |
| Unhealthy | < 150.0 | Red | 4 |
| Very Unhealthy | < 250.0 | Purple | 5 |
| Hazardous | ≥ 250.0 | Maroon | 6 |

## Potentiometer

The potentiometer on A4 controls the brightness of the NeoPixel strip in real time. It is read continuously during the `SAMPLE_RATE` wait interval between sensor readings, so brightness can be adjusted at any time without interrupting the sensor loop.

## Timing

| Constant | Value | Description |
|----------|-------|-------------|
| `SAMPLE_RATE` | 10s | Seconds between sensor readings |
| `ROLLING_RATE` | 120s | Window for rolling PM averages |
| `UPDATE_RATE` | 120s | Seconds between Adafruit IO uploads |

Rolling averages are maintained for PM2.5, PM10, and PM100 over the `ROLLING_RATE` window. Data is uploaded to Adafruit IO every `UPDATE_RATE` seconds (every 12 sample cycles).

Timing uses `adafruit_ticks` (`ticks_ms`, `ticks_add`, `ticks_less`) for rollover-safe operation. Note: CircuitPython intentionally initializes `ticks_ms` near the 29-bit rollover point (~536M ms) so that rollover bugs surface within the first 65 seconds — this is by design.

## Adafruit IO Feeds (group: `aqi`)

| Feed | Content |
|------|---------|
| `aqi.pm25` | PM2.5 rolling average |
| `aqi.pm10` | PM10 rolling average |
| `aqi.pm100` | PM100 rolling average |
| `aqi.temp` | Temperature (°F) |
| `aqi.humidity` | Relative humidity (%) |
| `aqi.level` | EPA AQI label |
| `aqi.log` | Startup parameters log |
| `aqi.details` | Per-size particle counts |

## Setup

1. Copy `settings.toml.example` to `settings.toml` and fill in your credentials
2. Copy all files to your CIRCUITPY drive
3. The board connects to WiFi, opens or creates the `aqi` feed group, and begins sampling

## Dashboard

A web dashboard is hosted on GitHub Pages at [https://mlehackett.github.io/aqi/dashboard.html](https://mlehackett.github.io/aqi/dashboard.html). It displays live AQI data pulled directly from Adafruit IO with a first-run login screen that saves credentials to `localStorage`. The background photo (`horizon.jpg`) is a view of the Multnomah Channel from Skyline Moorage & Marina in Portland, Oregon.

## Files

| File | Description |
|------|-------------|
| `code.py` | Main application |
| `lib/utilities.py` | `io_retry` decorator for Adafruit IO error handling |
| `settings.toml` | WiFi and Adafruit IO credentials (gitignored) |
| `dashboard.html` | GitHub Pages web dashboard |
| `horizon.jpg` | Background photo for dashboard |
