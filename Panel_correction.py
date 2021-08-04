import glob
import os
import exiftool
import micasense.imageset as imageset
import micasense.capture as capture
import micasense.metadata as metadata
import numpy as np


# =====================================================================
'''
Panel irradiance interpolation

Code used for radiometric calibration of micasense cameras (e.g.,
Altum) with two panels integration. Panel images captured before and
after each flight to provide an accurate representation of light
conditions during the flight!
'''
# =====================================================================


# Setting up your images path
# e.g., /home/wagner/Altum/05mar2020/
os.getcwd()
os.listdir()
images_dir = os.getcwd() + '/Images/'

# =====================================================================


# Reading micasense images
panel = sorted(glob.glob(images_dir + '/**/*.tif', recursive=True))

# panel images captured before the fly
panelNames_before = panel[0:6]  # edit for RedEdge-MX camera, panel[0:9]

# panel image captured after the fly
panelNames_after = panel[-6:]  # edit for RedEdge-MX camera, panel[-9:]

# Reading capture class
panelcap_before = capture.Capture.from_filelist(panelNames_before)
panelcap_after = capture.Capture.from_filelist(panelNames_after)

# Reflectance by band, calibrated values
panel_reflectance_by_band = panelcap_before.panel_albedo()
panel_reflectance_by_band

# =====================================================================
'''
Getting the information from the panel image before the flight

'''
# =====================================================================

# Irradiance by band obtained by the calibration panel
panel_irradiance_before = np.array(
    panelcap_before.panel_irradiance(panel_reflectance_by_band))

# Irradiance by band obtained in the DLS sensor
dls_irradiance_before = np.array(panelcap_before.dls_irradiance()[:-1])

# Correction fractions
dls_correction_before = panel_irradiance_before/dls_irradiance_before

# Reading metadata and getting the panel capture time
meta_before = metadata.Metadata(panelNames_before[0])
Time_before = meta_before.utc_time().hour + \
    (meta_before.utc_time().minute/60) + \
    (meta_before.utc_time().second/3600)

meta_before.get_all()

# =====================================================================
'''
Getting the information from the panel image after the flight

'''
# =====================================================================

# Irradiance by band obtained by the calibration panel
panel_irradiance_after = np.array(
    panelcap_after.panel_irradiance(panel_reflectance_by_band))

# Irradiance by band obtained in the DLS sensor
dls_irradiance_after = np.array(panelcap_after.dls_irradiance()[:-1])

# Correction fractions
dls_correction_after = panel_irradiance_after/dls_irradiance_after

# Reading metadata and getting the panel capture time
meta_after = metadata.Metadata(panelNames_after[0])
Time_after = meta_after.utc_time().hour + \
    (meta_after.utc_time().minute / 60) + \
    (meta_after.utc_time().second/3600)

meta_after.get_all()


# =====================================================================
'''
Linear interpolation of irradiance during the flight

'''
# =====================================================================

# Linear interpolation
m = (panel_irradiance_after-panel_irradiance_before)/(Time_after-Time_before)


def lin_interp(time):
    return (m*(time-Time_before)+panel_irradiance_before)*100


imgset = imageset.ImageSet.from_directory(images_dir)

for cap in imgset.captures:
    print("Opened Capture {} with bands {}".format(
        cap.uuid, [str(band) for band in cap.band_names()]))

imgset_ls = imgset.as_nested_lists()[0]
imgset_ls

dat = []
irr = []
for i in range(0, len(imgset_ls)):
    dat.append(imgset_ls[i][0].hour + (imgset_ls[i][0].minute/60) +
               (imgset_ls[i][0].second/3600))
    irr.append(imgset_ls[i][8:13])

irr_interp = []
for i in range(0, len(imgset_ls)):
    irr_interp.append(lin_interp(dat[i]))

irr_interp_ls = np.asarray(irr_interp).flatten()
irr_interp_ls_b = []

for i in range(0, len(irr_interp_ls)):
    irr_interp_ls_b.append(bytes(str(irr_interp_ls[i]), 'utf8'))

images = sorted(glob.glob(images_dir + '/**/*[12345].tif', recursive=True))
images_b = []

for i in range(0, len(images)):
    images_b.append(bytes(images[i], 'utf8'))


# =====================================================================
'''
Replacing values of irradiance interpolated in images metadata with Exiftool

'''
# =====================================================================

et = exiftool.ExifTool()
et.start()
for i in range(0, len(images_b)):
    et.execute(b'-Irradiance=' +
               irr_interp_ls_b[i], images_b[i], b'-overwrite_original')
    et.execute(b'-HorizontalIrradiance=' +
               irr_interp_ls_b[i], images_b[i], b'-overwrite_original')
    print('Calibrating image {}'.format(images_b[i]))

# =================================================================
