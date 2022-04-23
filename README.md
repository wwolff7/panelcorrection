# Radiometric calibration of Micasense camera images

Interpolating irradiance values of the Micasense panel during the drone flight
time and adding them into images' metadata.

Below, we go through the options to download and install a full working Python
environment for the job. For sake of convenience, the use of Anaconda
or miniconda environments is recommended.

## Installing [ExifTool](https://exiftool.org/), software for editing image metadata


```
wget https://cpan.metacpan.org/authors/id/E/EX/EXIFTOOL/Image-ExifTool-12.15.tar.gz
tar -xvzf Image-ExifTool-12.15.tar.gz
cd Image-ExifTool-12.15/
perl Makefile.PL
make test
sudo make install
```
For more information visit [exiftool install](https://exiftool.org/install.html)


## Cloning the **imageprocessing** repository at micasense GitHub page


```
git clone https://github.com/micasense/imageprocessing.git
cd imageprocessing
conda env create -f micasense_conda_env.yml

cd imageprocessing
conda activate micasense
python setup.py install
```
## or installing via pip in a virtual enviroment, for instance:

```
pyenv virtualenv 3.8.0 micasense
pip install git+https://github.com/micasense/imageprocessing.git
```

## Cloning the **panelcorrection** repository

```
cd ../
git clone https://github.com/wwolff7/panelcorrection.git
cd panelcorrection
```

For editing and replacing image metadata values the file **ExifTool_config** must
replace the original **.Exiftool_config** file. For example on Ubuntu:

```
cp ExifTool_config ~/.ExifTool_config
```
For more details please see my question on [ExifTool
forum](https://exiftool.org/forum/index.php?topic=10831.msg57671#msg57671).
Phil Harvey, ExifTool author help me a lot!

Finally, open the Panel_correction.py file and edit it with some python IDE (e.g., emacs,
vim, spyder, jupyter, atom, etc.). Just set up the path of your images and let the
panel capture before the flight as the first file and the panel capture after
the flight as the last file.


## Remarks

* Tested on Ubuntu 18.04 LTS for Altum camera.


## To-do

* Test on Ubuntu for RedEdge-MX camera.
* Test on Windows for Altum and RedEdge-MX cameras.
