import ee

def image_scaler(img):
    optical = img.select("SR_B.+").multiply(2.75e-5).add(-0.2)
    thermal = img.select("ST_B.+").multiply(0.00341802).add(149)

    img = img.addBands(optical, None, True).addBands(thermal, None, True)

    return img

def cloud_mask(img):
    qa = img.select("QA_PIXEL")
    
    cirrus = qa.bitwiseAnd((1 << 2)).eq(0)
    cloud = qa.bitwiseAnd((1 << 3)).eq(0)
    shadow = qa.bitwiseAnd((1 << 4)).eq(0)
    snow = qa.bitwiseAnd((1 << 5)).eq(0)
    
    img = (
        img.updateMask(cirrus)
           .updateMask(cloud)
           .updateMask(shadow)
           .updateMask(snow)
    )

    return img

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