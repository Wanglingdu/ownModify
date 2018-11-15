# coding:utf-8
from skimage import io, measure
import numpy as np
import cv2, copy, inspect, time

def report_cutter(img_path):
    ''' cut out the report of the whole ultra-sound image '''
    img_name = img_path.split("/")[-1]
    img = cv2.imread(img_path)
    img_copy = copy.deepcopy(img)
    img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    assert len(img_gray.shape) == 2
    img_1d = np.reshape(img_gray, (img_gray.shape[0]*img_gray.shape[1],1))
    img_1d = np.float32(img_1d)

    # k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0) # define criteria = (type,max_iter,epsilon)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _,labels,centers = cv2.kmeans(data=img_1d,K=2,bestLabels=None,criteria=criteria,attempts=10,flags=flags)
    assert len(centers) == 2
    if centers[0] > centers[1]:
        labels = 1 - labels # assure that report paper is white
    img_kmeans = np.reshape(labels, (img_gray.shape[0], img_gray.shape[1]))

    pad_zero = (50,50)
    img_augmented = np.zeros((img_kmeans.shape[0]+pad_zero[0]*2, img_kmeans.shape[1]+pad_zero[1]*2))
    img_augmented[pad_zero[0]:pad_zero[0]+img_kmeans.shape[0], pad_zero[1]:pad_zero[1]+img_kmeans.shape[1]] = img_kmeans[:]

    b = img_augmented
    b = (b!=0).astype(int) # mask all nonewhite regions
    b = measure.label(b)

    max_box_area = -1
    for region in measure.regionprops(b):
        if region.area > max_box_area:
            max_box_area = region.area
            minr, minc, maxr, maxc = region.bbox

    # convert cordinates to origin report range
    ominr = max(minr - pad_zero[0], 0)
    omaxr = min(maxr - pad_zero[0], img.shape[0])
    ominc = max(minc - pad_zero[1], 0)
    omaxc = min(maxc - pad_zero[1], img.shape[1])
    report_range = img[ominr:omaxr, ominc:omaxc, :]

    return img_name, report_range, ominr, ominc

def img_detector(img_path):
    img_name, report, ominr, ominc = report_cutter(img_path)
    img = report
    img_copy = copy.deepcopy(img)
    img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    assert len(img_gray.shape) == 2
    img_1d = np.reshape(img_gray, (img_gray.shape[0]*img_gray.shape[1],1))
    img_1d = np.float32(img_1d)

    # k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0) # define criteria = (type,max_iter,epsilon)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _,labels,centers = cv2.kmeans(data=img_1d,K=2,bestLabels=None,criteria=criteria,attempts=10,flags=flags)
    assert len(centers) == 2
    if centers[0] > centers[1]:
        labels = 1 - labels # assure that report paper is white
    img_kmeans = np.reshape(labels, (img_gray.shape[0], img_gray.shape[1]))

    b = img_kmeans
    b = (b!=1).astype(int) # mask all nonewhite regions
    b = measure.label(b)
    coordinates_dict = {}
    dists = []
    for region in measure.regionprops(b):
        if region.area < 10000:
            continue
        minr, minc, maxr, maxc = region.bbox
        width_height = float(maxc - minc) / float(maxr - minr)
        if not (width_height > 0.75 and width_height < 1.5):
            continue
        cor = (ominr+minr, ominc+minc, ominr+maxr, ominc+maxc)
        x = minc
        y = -1.0 * minr
        distance = abs(-1.0 * x + 6.0 * y) / 6.0827625
        coordinates_dict[distance] = cor
        dists.append(copy.deepcopy(distance))
    dists.sort()
    coordinates = []
    for s in dists:
        coordinates.append(coordinates_dict[s])
    return coordinates

def img_cutter(img_path, output_path, coordinates):
    # coordinates = img_detector(img_path)
    img = io.imread(fname=img_path)
    img_name = img_path.split("/")[-1]
    output_img_paths = []
    for i in range(len(coordinates)):
        minr, minc, maxr, maxc = coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]
        output_img_name = output_path + "/" + img_name[:-4] + "_" + str(i+1) + ".jpg"
        io.imsave(output_img_name, img[minr:maxr,minc:maxc,:])
        output_img_paths.append(output_img_name)
    return output_img_paths

def img_marker(img_path, output_path, coordinates):
    img = cv2.imread(img_path)
    img_name = img_path.split("/")[-1]
    output_img_path = output_path + "/" + img_name[:-4] + "_marked.jpg"
    for i in range(len(coordinates)):
        minr, minc, maxr, maxc = coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]
        cv2.rectangle(img,(minc, minr),(maxc, maxr),(0,0,255),3)
    cv2.imwrite(output_img_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return output_img_path

# if __name__ == "__main__":
#     img_path = "test/234.jpg"

#     cutted_output_path = "test/cutted"
#     marked_output_path = "test/marked"
#     coordinates = img_detector(img_path)
#     print coordinates
#     print img_cutter(img_path, cutted_output_path, coordinates)
#     print img_marker(img_path, marked_output_path, coordinates)
