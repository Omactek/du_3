import rasterio
import numpy
from rasterio.windows import Window
from rasterio.transform import Affine
from shapely.geometry import box
import numpy.ma
import sys
import argparse


#function that returns intersction of both rasters
def r_intersect(raster_1, raster_2):
    #creates bounding box of rasters
    bb_raster_1 = box(raster_1.bounds[0], raster_1.bounds[1], raster_1.bounds[2], raster_1.bounds[3])
    bb_raster_2 = box(raster_2.bounds[0], raster_2.bounds[1], raster_2.bounds[2], raster_2.bounds[3])

    #saves edge coordinates
    xminR1, yminR1, xmaxR1, ymaxR1 = raster_1.bounds
    xminR2, yminR2, xmaxR2, ymaxR2 = raster_2.bounds

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

def compute_masking_matrix(dmt, dmr, threeshold):
    masking_matrix = numpy.where(abs((dmt-dmr))<threeshold,1,numpy.nan)
    return masking_matrix

def create_mask(raster_1, raster_2, threeshold):
    with rasterio.open('mask.tif', 'w', **kwargs) as dst:
        slices = [(col_start, row_start, step, step) \
                            for col_start in list(range(0, raster_1.shape[0], 5)) \
                            for row_start in list(range(0, raster_2.shape[1], 5))
                ]

        for slc in slices:
                    mask = compute_masking_matrix(raster_1[(slc[1]):(slc[1] + 5), slc[0]:(slc[0] + 5)],raster_2[(slc[1]):(slc[1] + 5), slc[0]:(slc[0] + 5)], 1)
                    print(type(mask))
                    print(mask)

                    win = Window(slc[0], slc[1], mask.shape[1], mask.shape[0])

                    dst.write_band(1, mask.astype(rasterio.float32), window=win)

#otevření vsupních rasterů
def run(path_ras_1, path_ras_2):
    with rasterio.open(path_ras_1) as DMR:
        with rasterio.open(path_ras_2) as DMT:

            try:
                if DMR.crs == DMT.crs:
                    pass
                else:
                    sys.exit("Chosen rasters do not have the same coordinate systems. Please choose rasters with the same coordinate systems.")

            except rasterio.errors.CRSError(DMR):
                sys.exit("The DMR raster does not have a valid coordinate system.")
                    
            except rasterio.errors.CRSError(DMT):
                sys.exit("The DMT raster does not have a valid coordinate system.")
                            
            except rasterio.error.RasterioIOError:
                sys.exit("At least one of input files is not a raster format file. Please choose raster files.")
                
            except rasterio.errors.RasterioError():
                sys.exit("An unexpected error occurred. Please try again.")

            step = 256
            kwargs = DMR.meta
            kwargs.update(dtype=rasterio.float32, count=1, compress='lzw')


            transform, r1, r2 = r_intersect(DMR, DMT)
            create_mask(r1, r2, 1)

parser = argparse.ArgumentParser(description="Takes terrain and surface rasters.")
parser.add_argument('--surface', dest = "raster_1", required=True,
                    help='Path to DMR. (.tif format)')
parser.add_argument('--terrain', dest="raster_2", required=True,
                    help='Path to DMT. (.tif format)')
args = parser.parse_args()

run(args.raster_1, args.raster_2)
