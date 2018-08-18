import scipy
import numpy as np
from scipy import ndimage
import util

dir = "./static/book"

imagelist = util.scan_files_no_root(dir,slug="")
for imageinfo in imagelist:
    image = np.array(ndimage.imread(dir+'/'+imageinfo, flatten=False))

    my_image =scipy.misc.imresize(image, size=(200, 200))
    try:
        scipy.misc.toimage(my_image).save("static/image/"+imageinfo)
    except BaseException:
        print(imageinfo)
    

