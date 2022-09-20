import rasterio
from rasterio.windows import Window
from rasterio.transform import Affine


path_ras_1 = "raster_zkouska_2.tif"
path_ras_2 = "raster_zkouska_2.tif"


#otevření vsupních rasterů
with rasterio.open(path_ras_1) as DMR:
    with rasterio.open(path_ras_2) as DMT:

        step = 256
        kwargs = DMR.meta
        kwargs.update(dtype=rasterio.float32, count=1, compress='lzw')

        with rasterio.open('ndvi_w.tif', 'w', **kwargs) as dst:
            slices = [(col_start, row_start, step, step) \
                        for col_start in list(range(0, DMR.width, 5)) \
                        for row_start in list(range(0, DMR.height, 5))
            ]

            #vypočítat
            # for ji, window in src.block_windows(1):
            for slc in slices:
                win = Window(*slc)

                DMT_data = DMT.read(1, window=win).astype(float)
                vis_data = DMR.read(1, window=win).astype(float)+1

                ndvi = (DMT_data - vis_data) / (DMT_data + vis_data)

                write_win = Window(slc[0], slc[1], ndvi.shape[1], ndvi.shape[0])

                dst.write_band(1, ndvi.astype(rasterio.float32), window=write_win)