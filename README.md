# program_tai-Body_Length_evaluation
program_tai3-main_field_photo_texture_and_HSV_analysis
(These programs were created with outstanding contributions by Shion Yamada master's degree in Chiba University)

1. Make the folder name "preparation_before"
2. Store the target photo (.tiff) in the folder (example: 4.tif in the site)
   About 4.tif (The photo will be adjusted as follows)
   a) Draw a blue line to measure the whole body length
   b) Dotting the measuring points such as the end of the snout, pectoral fins, tail rays, and anus
3. Make the folder name "preparation_after"
4. python3.X.X preparation_program.py
5. The Python command automatically draws a vertical line perpendicular to the blue line, and the photo will be stored in the folder "preparation_after" (example: preparation_after.zip)
6. Mark the joining points at the top and bottom of the fish's body (using a color with RGB values different from the body and other backgrounds) in the photo (example: measurement_before.zip)
7. Make the folder name "measure_before" and store the photo with the joining points in the folder
8. python3.X.X measure_program.py
9. The measurement results will be described in the filename "output.xlsx"


