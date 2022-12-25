import ee

def renamer7(img: ee.Image) -> ee.Image:
    """
    Function to extract the Landsat 5 and 7 bands of interest and rename it
    to coloquial names.

    Parameters
    ----------
    img : ee.Image
        Image of interest to subset and rename.

    Returns
    -------
    img : ee.Image
        Image with bands filtereds and renamed.
    """
    # Define the original and the new names
    ori_names = ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "ST_B6"]
    new_names = ["BLUE", "GREEN", "RED", "NIR", "TEMPERATURE"]
    
    # Select the bands with the original names an rename them
    img = img.select(ori_names).rename(new_names)

    return img

def renamer8(img: ee.Image) -> ee.Image:
    """
    Function to extract the Landsat 8 bands of interest and rename it
    to coloquial names.

    Parameters
    ----------
    img : ee.Image
        Image of interest to subset and rename.

    Returns
    -------
    img : ee.Image
        Image with bands filtereds and renamed.
    """
    # Define the original and the new names
    ori_names = ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "ST_B10"]
    new_names = ["BLUE", "GREEN", "RED", "NIR", "TEMPERATURE"]
    
    # Select the bands with the original names an rename them
    img = img.select(ori_names).rename(new_names)

    return img

def calc_ndvi(img: ee.Image) -> ee.Image:
    """
    Function to calculate de NDVI in one image.

    Parameters
    ----------
    img : ee.Image
        Image of interest to calculate the NDVI.

    Returns
    -------
    img : ee.Image
        Image with NDVI calculated.
    """
    # Define the NDVI formula
    f = "(b('NIR')-b('RED'))/(b('NIR')+b('RED'))"
    
    # Calculate the NDVI
    ndvi = img.expression(f).rename("NDVI")

    # Add NDVI band to image
    img = img.addBands(ndvi)

    return img