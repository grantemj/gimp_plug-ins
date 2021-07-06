#!/usr/bin/python
from gimpfu import *

# Use this to set context settings
# Call `pdb.gimp_context_push()` before calling this function
# And call `pdb.gimp_context_pop()` once usage of this context is completed
def setContext(antialias=None,feather=None,featherRadius=None,merged=None,
               criterion=None,thresholdInt=None,transparent=None,diagonalNeighbors=None):
    if antialias != None:
        pdb.gimp_context_set_antialias(antialias)
    if feather != None:
        pdb.gimp_context_set_feather(feather)
    if featherRadius != None:
        pdb.gimp_context_set_feather_radius(featherRadius)
    if merged != None:
        pdb.gimp_context_set_sample_merged(merged)
    if criterion != None:
        pdb.gimp_context_set_sample_criterion(criterion)
    if thresholdInt != None:
        pdb.gimp_context_set_sample_threshold_int(thresholdInt)
    if transparent != None:
        pdb.gimp_context_set_sample_transparent(transparent)
    if diagonalNeighbors != None:
        pdb.gimp_context_set_diagonal_neighbors(diagonalNeighbors)

def python_delete_layer_backgrounds(img, layer, customtext, font, size, threshold, diagonal, inclBkgd):
    # Create new context copied from current context
    pdb.gimp_context_push()
    setContext(antialias=True,
               thresholdInt=threshold,
               diagonalNeighbors=diagonal)
    # pdb.gimp_invert(layer)
    # img = gimp.Image(1, 1, RGB)
    # layer = pdb.gimp_text_fontname(img, None, 0, 0, customtext, 10, True, size, PIXELS, font)
    # img.resize(layer.width, layer.height, 0, 0)
    # gimp.Display(img)
    # gimp.displays_flush()
    x,y = 0
    for lyr in img.layers:
        if lyr.visible:
            # Make selection at coordinate
            pdb.gimp_image_select_contiguous_color(img,2,lyr,x,y)
            # Delete selection (by floating and then removing layer)
            pdb.gimp_selection_float(lyr,0,0)
            img.remove_layer(img.floating_selection)
            # Unselect all
            pdb.gimp_selection_none(img)
            
    # Return previous context
    pdb.gimp_context_pop()

register(
	"python_delete_layer_backgrounds",
	"Uses the Fuzzy Select Tool to delete the selection on every visible layer based on current mouse position",
	"Uses the Fuzzy Select Tool to delete the selection on every visible layer based on current mouse position",
	"Emma Grant",
	"Emma Grant",
	"2021",
	"<Image>/Image/Custom/Delete Layer Backgrounds",
	"*",
	[
        # (PF_IMAGE, "image", "Input image", None),
        # (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_STRING, "customtext", "Text string", 'Scripting is handy!'),
        (PF_FONT, "font", "Font", "Sans"),
        (PF_SPINNER, "size", "Font size", 100, (1, 3000, 1)),
        (PF_SPINNER, "threshold", "Fuzzy Select Threshold", 20, (0,255,1)),
        (PF_BOOL, "diagonal", "Fuzzy Select Diagonal Neighbors", True),
        (PF_BOOL, "inclBkgd", "Include Background Layer", True),
	],
	[],
	python_delete_layer_backgrounds)

main()