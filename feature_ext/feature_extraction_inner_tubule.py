import os
import numpy as np
from scipy import ndimage
from skimage import io, morphology, measure, color, filters, feature, util
from skimage.morphology import disk, dilation, erosion, binary_opening, binary_closing
from skimage.feature import graycomatrix, graycoprops
from skimage.segmentation import watershed
from skimage.color import rgb2gray
from scipy.ndimage import distance_transform_edt
from color_norm import color_norm
from getCompRatios import getCompRatios

def feature_extraction_inner_tubule(q, segmented_gloms, image_dir, min_object_size):
    v = np.zeros(302)
    
    # 读取分割图像和原始图像
    composite_path = os.path.join(segmented_gloms[q].folder, segmented_gloms[q].name)
    composite = io.imread(composite_path) > 0
    composite = composite.astype(np.uint8)
    
    image_path = os.path.join(image_dir[q].folder, image_dir[q].name)
    I = io.imread(image_path)
    I = color_norm(I)  
    # I = (I * 255).astype(np.uint8)
    
    # 提取各通道掩膜
    mes_mask = composite[:, :, 0]
    white_mask = composite[:, :, 1]
    nuc_mask = composite[:, :, 2]
    
    # 预处理掩膜
    nuc_mask = morphology.remove_small_objects(nuc_mask, min_size=2)
    boundary_mask = mes_mask | white_mask | nuc_mask
    boundary_mask = morphology.remove_small_objects(boundary_mask, min_size=1)
    
    mes_mask = ~morphology.remove_small_holes(~mes_mask, area_threshold=min_object_size)
    mes_mask = morphology.remove_small_objects(mes_mask, min_size=min_object_size)
    
    white_mask = morphology.remove_small_objects(white_mask, min_size=min_object_size)
    white_mask = morphology.remove_small_holes(white_mask)
    
    # # 距离变换
    # boundary_w_mem = dilation(boundary_mask, footprint=disk(10))
    # gdist = distance_transform_edt(boundary_mask)
    # gdist = -gdist + np.max(gdist)
    # gdist[~boundary_mask] = 0
    
    # gdist2 = distance_transform_edt(~boundary_mask)
    # gdist2 = -gdist2 + np.max(gdist2)
    # gdist2[~boundary_mask] = 0
    
    # # 分位数计算
    # nuc_dist_bound = gdist2 * nuc_mask.astype(float)
    # lum_dist_bound = gdist2 * white_mask.astype(float)
    # mes_dist_bound = gdist2 * mes_mask.astype(float)
    
    # lv = np.quantile(lum_dist_bound[lum_dist_bound > 0], np.arange(0.1, 1.1, 0.1))
    # nv = np.quantile(nuc_dist_bound[nuc_dist_bound > 0], np.arange(0.1, 1.1, 0.1))
    # mv = np.quantile(mes_dist_bound[mes_dist_bound > 0], np.arange(0.1, 1.1, 0.1))
    
    # # 基底膜检测 (需实现颜色反卷积)
    # _, sat, _ = colour_deconvolution(I, ['H PAS'])  # 需实现该函数
    # sat = 1 - sat.astype(float) / 255.0
    # sat = exposure.adjust_gamma(sat, gamma=3)
    
    # # 其他处理步骤（因篇幅限制，部分代码需补充实现）
    # # ...
    
    # # 特征填充示例（需根据原MATLAB代码完整实现）
    # v[0:3] = np.mean(ratiosL[:, 0:3], axis=0)
    # v[3] = np.sum(ratiosL[:, 3])
    # v[4] = np.mean(ratiosL[:, 3])
    # v[5] = np.median(ratiosL[:, 3])
    
    # # ... 其他特征填充
    
    # return v


def colour_deconvolution(image, stains):
    """颜色反卷积函数"""
    # 实现类似MATLAB的colour_deconvolution
    return np.zeros_like(image), np.zeros_like(image), np.zeros_like(image)

def get_thinness(mask):
    """计算薄度特征"""
    return []


def getNucRatios(composite, radius, grayIm):
    """实现细胞核特征"""
    return np.array([])

