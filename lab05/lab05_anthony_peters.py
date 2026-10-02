import arcpy

# Get tool parameters
garage_points = arcpy.GetParameterAsText(0)
buildings = arcpy.GetParameterAsText(1)
buffer_distance = arcpy.GetParameterAsText(2)

# Buffer the garages
garage_buffered = arcpy.GetParameterAsText(3)

arcpy.Buffer_analysis(
    garage_points,
    garage_buffered,
    buffer_distance
)

# Intersect the buffer with the buildings
intersection_output = arcpy.GetParameterAsText(4)

arcpy.Intersect_analysis(
    [garage_buffered, buildings],
    intersection_output,
    "ALL"
)
