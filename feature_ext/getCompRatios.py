import numpy as np
from skimage.measure import label, regionprops_table, regionprops
from skimage.morphology import convex_hull_image
from skimage.feature import graycomatrix, graycoprops

def get_comp_ratios(comp_ob, inte, min_object_size):
    target_mask = comp_ob[..., 0].astype(bool)
    labeled = label(target_mask)
    props = regionprops_table(labeled, properties=('label', 'area'))
    valid_labels = props['label'][props['area'] > min_object_size]
    filtered_mask = np.isin(labeled, valid_labels)
    labeled_clean, comp_num = label(filtered_mask, return_num=True) #comp_num是连通域的个数
    ratios = np.zeros((comp_num, 4))
    glcm = graycomatrix(inte.astype(np.uint8), distances=[1], angles=[0],symmetric=True, normed=True)

    s = {
        'contrast': graycoprops(glcm, 'contrast')[0, 0],
        'correlation': graycoprops(glcm, 'correlation')[0, 0],
        'energy': graycoprops(glcm, 'energy')[0, 0],
        'homogeneity': graycoprops(glcm, 'homogeneity')[0, 0]
    }

    regions = regionprops(labeled_clean)
    for i, reg in enumerate(regions):
        comp = reg.image #与边界框大小相同的切片二进制区域图像
        minr, minc, maxr, maxc = reg.bbox #r-row,c-col
        abs_mask = np.zeros_like(labeled_clean, dtype=bool)
        abs_mask[minr:maxr, minc:maxc] = comp

        ch  = convex_hull_image(abs_mask)
        cco = comp_ob[minr:maxr, minc:maxc, 1:3].copy()
        cco[~ch[minr:maxr, minc:maxc]] = 0
        cco_sum = cco.sum(axis=(0,1))

        ratios[i, 0] = reg.area / reg.convex_area #area-按像素面积缩放的区域像素数; convex_area-包围该区域的最小凸多边形
        ratios[i, 1] = cco_sum[0] / reg.area
        ratios[i, 2] = cco_sum[1] / reg.area
        ratios[i, 3] = reg.area
    
    return ratios, s, comp_num

if __name__ == "__main__":
    import cv2
    comp_ob = cv2.imread("/Users/xuanyu/Desktop/matlab/matlab/test/1_S_5/Glomeruli/Images/1_S_5_0.jpeg")
    # comp_ob = (np.random.rand(256,256,3) > 0.9).astype(np.uint8)
    inte    = np.random.randint(0, 256, (256, 256)).astype(np.uint8)
    ratios, s, comp_num = get_comp_ratios(comp_ob, inte, 10)
    print(ratios)
    print(s)
    print(comp_num)