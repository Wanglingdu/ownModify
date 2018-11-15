from skimage import io, measure
import numpy as np
import cv2, copy

def img_detector(img_path):
    ''' return the coordinate of each ultra-sound image '''
    img = io.imread(fname=img_path)
    img1 = copy.deepcopy(img)
    img1[img > 100] = 255
    a = img1[:,:,0]
    b = measure.label(a)

    label = b[b.shape[0]-10, b.shape[1]-10]

    b = (b!=label).astype(int) # mask all nonewhite regions
    b = measure.label(b) # seperate every region

    coordinates = []
    for region in measure.regionprops(b):
        if region.area < 10000:
            continue
        minr, minc, maxr, maxc = region.bbox
        coordinates.append((minr, minc, maxr, maxc))
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

if __name__ == "__main__":
    img_path = "test/0913_2.jpg"
    cutted_output_path = "test/cutted"
    marked_output_path = "test/marked"
    coordinates = img_detector(img_path)
    print img_cutter(img_path, cutted_output_path, coordinates)
    print img_marker(img_path, marked_output_path, coordinates)
