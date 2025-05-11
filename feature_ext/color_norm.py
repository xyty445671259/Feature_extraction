import numpy as np 
from skimage.color import rgb2lab, lab2rgb
import cv2
def color_norm(source_glom):
    stats = np.array([
        [75.86, 13.238, -11.870],
        [15.174, 8.348, 7.593]
    ])

    m_l, m_a, m_b = stats[0]
    s_l, s_a, s_b = stats[1]

    source_glom_float = source_glom.astype(np.float32)/255.0
    source_lab = rgb2lab(source_glom_float)

    sourceL = source_lab[:, :, 0]
    sourceA = source_lab[:, :, 1]
    sourceB = source_lab[:, :, 2]
    m1 = np.mean(sourceL)
    m2 = np.mean(sourceA)
    m3 = np.mean(sourceB)

    std1 = np.std(sourceL) #默认ddof=0，整体估计
    std2 = np.std(sourceA)
    std3 = np.std(sourceB)

    normalized_lab = np.empty_like(source_lab)
    normalized_lab[:, :, 0] = (sourceL - m1) * (s_l / std1) + m_l
    normalized_lab[:, :, 1] = (sourceA - m2) * (s_a / std2) + m_a
    normalized_lab[:, :, 2] = (sourceB - m3) * (s_b / std3) + m_b

    normalized_rgb = lab2rgb(normalized_lab) * 255.0
    return normalized_rgb.astype(np.uint8)
    

# if __name__ == "__main__":
#     source_glom = cv2.imread("/Users/xuanyu/Desktop/matlab/matlab/test/1_S_5/Glomeruli/Images/1_S_5_0.jpeg")
#     normalized_glom = color_norm(source_glom)
#     cv2.imshow("source_glom", source_glom)
#     cv2.imshow("normalized_glom", normalized_glom)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()