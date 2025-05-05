# Introduction
Sony cameras have been infamous for having "star eater" processing on their RAW files which makes them basically unusable for any serious astrophotography.
Having recently bought an A6700, I wanted to check if this is still the case. This code reproduces the work of Mark Shelley done [here](https://www.markshelley.co.uk/Astronomy/raw_data_filtering.html).

# Environment
Use UV to setup your Python environment, the PyQT requirements are for when running on WSL, you'll also need the following to get matplotlib to show charts correctly:
* `sudo apt install qt6-base-dev`
* `sudo apt install libxcb-cursor-dev`

# Other Links
This work prompted by this thread on [Cloudy Nights](https://www.cloudynights.com/topic/902676-sony-a7r5-no-longer-has-sony-star-eater/)