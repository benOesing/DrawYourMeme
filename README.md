# DrawYourMeme
This project takes any image, binarizes it and creates a GIF, where the image gets drawn part for part, according to the user input.
![image](dog.gif?raw=true)
## Setup:
1. This project uses plain Javascript, PHP and Python 3.8.5 (currently). Downloading PHP and Python is mandatory.
2. PHP allows to create a simple development server by executing the command: `php -S 127.0.0.1:8000` next to the index.html file.
3. The program can be accessed on the address: `127.0.0.1:8000` until the server gets closed.
## How it works:
1. The upload.php script is called, which saves the image in the upload folder.
2. The image gets binarized and the [Floyd-Steinberg][Dithering] dithering gets calculated as an alternative visualization.
3. The user interacts with the interactive webpage to determine his wanted result.
4. The exec.php script gets called, which tries to prevent any malicious attack before calling the Python script that will draw the GIF.
    
    4.1. All the set pixels get collected and sorted to follow the selected draw mode.
    
    4.2. A sequence of (fps * seconds) images gets drawn and combined to a GIF.
5. The GIF gets saved for access.
6. Clean up, delete the sequence of images, keeping the original image, if the user wants to draw the same image with different settings and the resulting gif to allow linking and access.
## Disclaimer
While trying to defend against every malicious attack, the PHP scripts still offer a significant risk for malicious code execution.
### Improvements
This code was written for a fun project and to get familiar with Python, PHP and some Javascript a few years ago. The code was hosted on an actual server, resulting in the structure of this project. The Python script originally was written in an deprecated version of python, so some features dont work yet.
- HTML is broken
- Pythonscript needs to be adapted to 3.8.x
- Pythonscript needs to get structured.
- Read deeper into security to prevent malicious code execution.

[Dithering]: https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering