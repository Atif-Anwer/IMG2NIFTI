<a name="readme"></a>

<!-- [![Contributors][contributors-shield]][contributors-url] -->
![Python][python-shield]
<!-- [![Stargazers][stars-shield]][stars-url] -->

<!-- GETTING STARTED -->
## Introduction

Python script to convert Zeiss .img files to NIFTI format.
- The script requires thepath to a root folder containing the *.img image files.
- The converted nifti files (*.ni.gz) are saved in the same folder as the path provided.
- The File names of the coverted nifti files are the same as the original img files.
- Optionally, the script can also save individual slices in separate folders created for each *.img file
- A mp4 video of the img file can also be saved if required
- Optionally, random 50 slices in the image can also be viewed.

## Requirements
- pip
- natsort>=8.2.0
- nibabel>=4.0.2
- numpy>=1.19.5
- oct_converter>=0.5.0
- Pillow>=9.4.0

<!-- USAGE EXAMPLES -->
## Installation

1. To install the required dependencies, just run: `pip install -r requirements.txt`

## Usage

**Default usage**: In a terminal, just run the following command (where *path-to-folder* is the path to the root folder containing all the Zeiss *.img files)

 `python img_to_nifti.py --path /path-to-folder/`

**Usage with flags**: Optional flags can be provided for functions described below.

  `python img_to_nifti.py --path /path-to-folder/ --preview True --save_video True --save_slices True`

* --help: Displays the flags and other information
* --preview : (Default False) Preview random 50 slices from the img file before conversion
* --save_video: (Default False) Save an mp4 video of the img file
* --save_slices: (Default False) For all the img files, ave all slices as individual PNG files in sub-folders (created automatically)



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/Python-3.7-blue?style=for-the-badge&logo=appveyor
[tf-shield]: https://img.shields.io/badge/Tensorflow-2.8-orange?style=for-the-badge&logo=appveyor

[issues-shield]: https://img.shields.io/github/issues/Atif-Anwer/SpecSeg?style=for-the-badge
[issues-url]: https://github.com/Atif-Anwer/SpecSeg/issues
[license-shield]: https://img.shields.io/badge/License-CC-brightgreen?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/atifanwer/

<!-- Soruce: https://github.com/othneildrew/Best-README-Template/pull/73 -->