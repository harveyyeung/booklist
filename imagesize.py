import scipy
import numpy as np
from scipy import ndimage
import util

dir = "./static/data"

imagelist = util.scan_files_no_root(dir)
for imageinfo in imagelist:
    image = np.array(ndimage.imread(dir+'/'+imageinfo, flatten=False))
    print(image.shape)
    my_image =scipy.misc.imresize(image, size=(200, 200))
    print(my_image.shape)
    scipy.misc.toimage(my_image).save("static/image/"+imageinfo)
