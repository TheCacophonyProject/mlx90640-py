# mlx90640-py

## Install
- Start from base Thermal Camera RPi image
- apt update and upgrade
- Add to salt nodegroups dev and blacklist
- Change I2C speed on RPi to 1000000
- Install python3 and pip3
- `sudo apt-get install libatlas-base-dev`
- Make virtual env and run pip -r requirements
- Disable adn stop `thermal-uploader` and `leptond`
- Install version of `thermal-recorder` that can handle the mlx90640 data.
