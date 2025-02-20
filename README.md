# Calcul du volume

Le script calcul automatiquement le volume de DoDs (`.tif`) présent dans des
sous-dossiers d'un dossier principal. Par exemple, le script calculera le volume
de chaque ficiers dans Katlahraun puis pour chaque fichiers dans Kerling etc.
(cf. ci-dessous).

```
dir_dod_clean
    ├── Katlahraun
    │   ├── Katlahraun_2015_2016_DOD_mask_cordon.tif
    │   ├── Katlahraun_2016_2017_DOD_mask_cordon.tif
    │   ├── Katlahraun_2017_2018_DOD_mask_cordon.tif
    │   ├── Katlahraun_2018_2019_DOD_mask_cordon.tif
    │   ├── Katlahraun_2019_2021_DOD_mask_cordon.tif
    │   ├── Katlahraun_2021_2022_DOD_mask_cordon.tif
    │   └── Katlahraun_2022_2023_DOD_mask_cordon.tif
    ├── Kerling
    │   ├── Kerling_2015_2016_DOD_mask_cordon.tif
    │   ├── Kerling_2016_2017_DOD_mask_cordon.tif
    │   ├── Kerling_2017_2018_DOD_mask_cordon.tif
    │   ├── Kerling_2018_2021_DOD_mask_cordon.tif
    │   ├── Kerling_2021_2022_DOD_mask_cordon.tif
    │   └── Kerling_2022_2023_DOD_mask_cordon.tif
```

## Exécution

On lance le scipt dans la console Python de QGIS. Ne pas oublier de changer les
chemins et d'installer `pandas` et `glob`.

