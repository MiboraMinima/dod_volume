from qgis.PyQt.QtCore import (QCoreApplication, QVariant)
from qgis.analysis import QgsRasterCalculatorEntry, QgsRasterCalculator
from qgis.core import *
import processing

import os
import re
import pandas as pd
import glob
import time

# ==============================================================================
# PARAMETRES
# ==============================================================================

# INPUT
# Dir order effect
dir_dod_clean = 'path'
# dir_dod_unclean = 'path'

dirs_base = [dir_dod_clean] # a list if you want to pass multiple dir

# Threshol (m)
threshold = 0.125

# a list of site name, they have to exactly correspond to the name of folders
places = ['Katlahraun', 'Kerling', 'Selatangar', 'Reykjanesta']

# OUTPUT
# Dossier de destination des DODs
dir_stat = "path"

# ==============================================================================
# PROCESS
# ==============================================================================

# Initialize time counter
start_time = time.time()

# Find DOD
for dbase in dir_dod_clean:
    # Get all .tif in dbase
    files = glob.glob(f"{dbase}/**/*.tif")
    # print(files)
    dict_vol = {}
    for file in files:
        filename = os.path.basename(file)
        dirname = os.path.basename(os.path.dirname(file))
        if dirname in places:
            place = dirname
            print(f"Current place is : {place}")
            if re.search(rf'{place}', filename):
                date = re.search(r'(\d{4}_\d{4})', filename).group(1)
                print(f"Current date is {date}")
                print(f"layer name is : {filename}")

                # Raster zonal statistic
                if dbase.endswith('BORDER'):
                    dod_vol_path = f'{dir_stat}/{place}/{place}_{date}_volume_clean.csv'
                else:
                    dod_vol_path = f'{dir_stat}/{place}/{place}_{date}_volume_unclean.csv'

                print(f"Output path : {dod_vol_path}")

                if os.path.exists(dod_vol_path):
                    print('Statistics already exists fo the DOD')
                else:
                    print('Computing statistics')
                    dod_cut = QgsRasterLayer(file)

                    params = {
                        'INPUT': dod_cut,
                        'BAND': 1,
                        'ZONES': dod_cut,
                        'ZONES_BAND': 1,
                        'REF_LAYER': 0,
                        'OUTPUT_TABLE': dod_vol_path
                    }

                    processing.run("native:rasterlayerzonalstats", params)

                # Compute global statistics
                dod_vol = pd.read_csv(dod_vol_path)

                # Filter by threshold
                dod_vol = dod_vol.loc[(dod_vol['zone'] > threshold) |
                                      (dod_vol['zone'] < (threshold - (threshold*2)))]
                dod_vol['vol'] = dod_vol['sum'] * dod_vol['m2']

                dod_vol.to_csv(dod_vol_path, index=False)

                # Compute sum of positif and negatives values and total
                tot_pos = dod_vol.loc[dod_vol['vol'] > 0, 'vol'].sum()
                print(f"Total volume gained : {tot_pos} m3")
                tot_neg = dod_vol.loc[dod_vol['vol'] < 0, 'vol'].sum()
                print(f"Total volume loose : {tot_neg} m3")
                net = tot_pos + tot_neg
                print(f"Net volume : {net} m3")
                tot = tot_pos + abs(tot_neg)
                print(f"Total volume : {tot} m3")

                # Register current DOD date
                df_vol = pd.DataFrame({
                    'site': place,
                    'tot': tot,
                    'tot_pos': tot_pos,
                    'tot_neg': tot_neg,
                    'net': net,
                    'date': date
                }, index=[0])

                dict_name = f'{place}_{date}'
                dict_vol[dict_name] = df_vol

    df_vol_all = pd.concat(dict_vol)
    for site in places:
        df = df_vol_all.loc[df_vol_all['site'] == site]
        if dbase.endswith('BORDER'):
            df.to_csv(f'{dir_stat}/volume_{site}_clean.csv', index=False)
        else:
            df.to_csv(f'{dir_stat}/volume_{site}_unclean.csv', index=False)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")
