import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, footprint_rectangle, opening
from skimage.color import label2rgb
import cv2
image = data.coins()

thresh = threshold_otsu(image)
bw = closing(image>thresh, footprint_rectangle((3,3)))
bw = clear_border(bw)
label_image = label(bw)
image_label_overlay = label2rgb(label_image, image=image, bg_label=0)


# fig, (ax0, ax1, ax2, ax3) = plt.subplots(1, 4, figsize=(8, 4))

# ax0.imshow(image, cmap='gray')
# ax0.set_title('Original')
# ax0.axis('off')

# ax1.imshow(bw, cmap='gray')
# ax1.set_title('Binary')
# ax1.axis('off')

# ax2.imshow(label_image, cmap='gray')
# ax2.set_title('Labeled')
# ax2.axis('off')

# ax3.imshow(image_label_overlay)
# ax3.set_title('Labeled Regions')
# ax3.axis('off')

# plt.tight_layout()
# plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(image_label_overlay)
for region in regionprops(label_image):
    # take regions with large enough areas
    if region.area >= 100:
        # draw rectangle around segmented coins
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle(
            (minc, minr),
            maxc - minc,
            maxr - minr,
            fill=False,
            edgecolor='red',
            linewidth=2,
        )
        ax.add_patch(rect)

ax.set_axis_off()
plt.tight_layout()
plt.show()