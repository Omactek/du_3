from cmath import pi
import rasterio
import numpy
from rasterio.windows import Window
from rasterio.transform import Affine
from shapely.geometry import box
import numpy.ma
import sys
import argparse
from math import tan


#function that returns intersction of both rasters
def r_intersect(raster_1, raster_2):
    #creates bounding box of rasters
    bb_raster_1 = box(raster_1.bounds[0], raster_1.bounds[1], raster_1.bounds[2], raster_1.bounds[3])
    bb_raster_2 = box(raster_2.bounds[0], raster_2.bounds[1], raster_2.bounds[2], raster_2.bounds[3])

    #saves edge coordinates
    xminR1, yminR1, xmaxR1, ymaxR1 = raster_1.bounds
    xminR2, yminR1, xmaxR1, ymaxR2 = raster_2.bounds

    #creates intersection and transforms it
    intersection = bb_raster_1.intersection(bb_raster_2)
    transform = Affine(raster_1.res[0], 0.0, intersection.bounds[0], 0.0, -raster_1.res[1], intersection.bounds[3])

    #saves edge coordinates of the intersection
    p1Y = intersection.bounds[3] - raster_1.res[1]/2
    p1X = intersection.bounds[0] + raster_1.res[0]/2
    p2Y = intersection.bounds[1] + raster_1.res[1]/2
    p2X = intersection.bounds[2] - raster_1.res[0]/2

    #calculates indexes of first and last pixels of row and col
    row1R1 = int((ymaxR1 - p1Y)/raster_1.res[1])
    row1R2 = int((ymaxR2 - p1Y)/raster_2.res[1])
    col1R1 = int((p1X - xminR1)/raster_1.res[0])
    col1R2 = int((p1X - xminR2)/raster_1.res[0])
    row2R1 = int((ymaxR1 - p2Y)/raster_1.res[1])
    row2R2 = int((ymaxR2 - p2Y)/raster_2.res[1])
    col2R1 = int((p2X - xminR1)/raster_1.res[0])
    col2R2 = int((p2X - xminR2)/raster_1.res[0])

    #calculates width and height of intersection
    width_1 = col2R1 - col1R1 + 1
    width_2 = col2R2 - col1R2 + 1
    height_1 = row2R1 - row1R1 + 1
    height_2 = row2R2 - row1R2 + 1

    #creates matrices based on intersection
    raster_1_inter = raster_1.read(1, window=Window(col1R1, row1R1, width_1, height_1))
    raster_2_inter = raster_2.read(1, window=Window(col1R2, row1R2, width_2, height_2))

    return transform, raster_1_inter, raster_2_inter


def create_rasters(raster_1, raster_2, threeshold, step, key_arg):
    with rasterio.open('mask.tiff', 'w', **key_arg) as mask_dst:
        with rasterio.open('slopes.tiff', 'w', **key_arg) as slopes_dst:
            slices = [(col_start, row_start, step, step) \
                                for col_start in list(range(0, raster_1.shape[0], step)) \
                                for row_start in list(range(0, raster_2.shape[1], step))]

            #cuts raster to blocks
            for slc in slices:
                raster_1_block = raster_1[(slc[1]):(slc[1] + step), slc[0]:(slc[0] + step)]
                raster_2_block = raster_2[(slc[1]):(slc[1] + step), slc[0]:(slc[0] + step)]

                #creates matrix, if the difference in Z is lower than threeshold saves 1 else saves nan
                mask = numpy.where(abs((raster_1_block - raster_2_block)) < threeshold,1,numpy.nan)

                #writes mask matrix to raster
                win = Window(slc[0], slc[1], mask.shape[1], mask.shape[0])
                mask_dst.write_band(1, mask.astype(rasterio.float32), window=win)

                #creates matrix where if value in mask equals 1 saves dmt value else saves nan
                extracted_matrix = numpy.where(mask == 1, raster_2_block, numpy.nan)

                #creates matrix of slope
                x,y = numpy.gradient(extracted_matrix, 1)
                slope = numpy.sqrt(x ** 2 + y ** 2)
                slope_deg = numpy.arctan(slope)*(180/pi)

                #writes slope matrix to raster
                slopes_dst.write_band(1, slope_deg.astype(rasterio.float32), window=win)

#otevření vsupních rasterů
def run(path_ras_1, path_ras_2):
    with rasterio.open(path_ras_1) as DMP:
        with rasterio.open(path_ras_2) as DMT:

            try:
                if DMP.crs == DMT.crs:
                    pass
                else:
                    sys.exit("Chosen rasters do not have the same coordinate systems. Please choose rasters with the same coordinate systems.")

            except rasterio.errors.CRSError():
                sys.exit("The raster does not have a valid coordinate system.")
                            
            except rasterio.error.RasterioIOError:
                sys.exit("At least one of input files is not a raster format file. Please choose raster files.")
                
            except rasterio.errors.RasterioError():
                sys.exit("An unexpected error occurred. Please try again.")

            kwargs = DMP.meta
            kwargs.update(dtype=rasterio.float32, count=1, compress='lzw')

            transform, r1, r2 = r_intersect(DMP, DMT)
            kwargs.update(driver="GTiff", dtype=rasterio.float32, compress='lzw', transform = transform, height = r2.shape[0], width = r2.shape[1])

            create_rasters(r1, r2, 1, 17800, kwargs)

parser = argparse.ArgumentParser(description="Takes terrain and surface rasters.")
parser.add_argument('--surface', dest = "raster_1", required=True,
                    help='Path to DMP. (.tif format)')
parser.add_argument('--terrain', dest="raster_2", required=True,
                    help='Path to DMT. (.tif format)')
args = parser.parse_args()


run(args.raster_1, args.raster_2)