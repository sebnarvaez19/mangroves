import ee

def renamer7(img):
    ori_names = ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "ST_B6"]
    new_names = ["BLUE", "GREEN", "RED", "NIR", "TEMPERATURE"]
    
    img = img.select(ori_names).rename(new_names)

    return img

def renamer8(img):
    ori_names = ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "ST_B10"]
    new_names = ["BLUE", "GREEN", "RED", "NIR", "TEMPERATURE"]
    
    img = img.select(ori_names).rename(new_names)

    return img

def calc_ndvi(img):
    f = "(b('NIR')-b('RED'))/(b('NIR')+b('RED'))"
    ndvi = img.expression(f).rename("NDVI")

    img = img.addBands(ndvi)

    return img