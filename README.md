# SlidesLive Downloader
> A simple tool to crawl slides on https://slideslive.com/ and merge them into a pdf.
## Requirements
- Python packages specified in `requirements.txt`.
- Chrome driver file under the `driver` folder (needs to download the driver that match the version of the chrome browser on your computer, and default version under this folder is 86.0.4240.22).
## Usage
- `python main.py $slides_id$`, where `$slides_id$` refers to the string of digits in the path to slides you want to download on slideslive site.
## Notice
- **Downloading slides played on live are NOT supported.**
