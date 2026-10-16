# Anthony Peters
# GEOG 676 - Lab 7: Raster Analysis

import os
import arcpy
from arcpy.sa import Hillshade, Slope

arcpy.env.overwriteOutput = True

# Set input and output paths
workspace = r"C:\GEOG 676 Lab7"
landsat_folder = os.path.join(workspace, "landsat4")
dem = os.path.join(workspace, "dem", "dem_30m.tif")

# Arrange bands in red, green, blue order
bands = [
    os.path.join(landsat_folder, "red.tif"),
    os.path.join(landsat_folder, "green.tif"),
    os.path.join(landsat_folder, "blue.tif")
]

# Create a three-band composite
composite = os.path.join(workspace, "composite.tif")
arcpy.management.CompositeBands(bands, composite)
print("Composite raster created.")

# Use Spatial Analyst for terrain analysis
arcpy.CheckOutExtension("Spatial")

try:
    # Project the DEM from degrees to meters
    projected_dem = os.path.join(workspace, "dem_projected.tif")
    arcpy.management.ProjectRaster(
        dem,
        projected_dem,
        arcpy.SpatialReference(32614),
        "BILINEAR",
        30
    )
    dem = projected_dem

    # Create hillshade using the projected DEM
    hillshade = Hillshade(dem, 315, 45, "NO_SHADOWS", 1)
    hillshade.save(os.path.join(workspace, "hillshade.tif"))
    print("Hillshade raster created.")

    slope = Slope(dem, "DEGREE", 1)
    slope.save(os.path.join(workspace, "slope.tif"))
    print("Slope raster created.")

finally:
    arcpy.CheckInExtension("Spatial")

print("Lab 7 complete!")
