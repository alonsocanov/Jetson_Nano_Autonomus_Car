# Jetson Nano Self Drivin Car

This project aims to make a driveless jetson Nano car

## Material

- Jetson Nano
- Camera
- Arduino Uno
- MakerFocus I2C OLED Display module 0.91 inch I2C SSD1306
- Waveshare IMX219-83 Stereo Camera

## Libraries

Oled display:

- Adafruit-SSD1306
- board
- busio
- Pillow

## Waveshare IMX219-83 Stereo Camera

The documentation for the [Waveshare IMX219-83 Stereo Camera](https://www.waveshare.com/wiki/IMX219-83_Stereo_Camera)

If the images from the camera are red install in the previous link there are steps to correct it. Also the steps copied are:

```bash
wget https://www.waveshare.com/w/upload/e/eb/Camera_overrides.tar.gz
tar zxvf Camera_overrides.tar.gz
sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp
```

## Jetson Nano connection to MakerFocus I2C OLED Display

| Jetson Nano   | I2C OLED Display |
| :------------ | ---------------: |
| Pin 1 (3.3 V) |          Pin VCC |
| Pin 3 (SDA)   |          Pin SDA |
| Pin 5 (SCL)   |          Pin SCL |
| Pin 6 (GND)   |          Pin GND |
