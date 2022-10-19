import cv2

cap = cv2.VideoCapture(r'D:\AUT\COMP702 笔记\Project\frames\video.mp4')
bgsubmog = cv2.bgsegm.createBackgroundSubtractorMOG()  # remove background

# Video Morphology
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# Save vehicle hub information
cars = []
# Counting cars
car_n = 0

while True:
    ret, frame = cap.read()

    if ret:
        '''
        视频预处理阶段
        '''
        # Greyscale Treatment
        # Image grayscale processing can be used as a preprocessing step for image segmentation, image recognition, and image analysis.
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gaussian denoising -Gaussian filtering is a linear smoothing filter which is suitable for eliminating Gaussian noise and widely used in image denoising.
        # It can simply be understood that Gaussian filter denoising is the weighted averaging of pixel values across an image, with values for each pixel being obtained by weighted averaging their own values and those of other pixels in the neighborhood
        blur = cv2.GaussianBlur(frame, (3, 3), 5)  # GaussianBlur().Gaussian filter is a linear smoothing filter which is suitable for eliminating Gaussian noise and widely used in image processing.
        mask = bgsubmog.apply(blur)  # remove background
        cv2.imshow('video', mask)

        # Corrosion -can be more accurate in colour tracing, with less colour interference
        erode = cv2.erode(mask, kernel)  # erode()Image erosion, combined with Gaussian blurring, can make the image more colourful

        # Expansions are morphological operations, called morphologies, that change the shape of an object, figuratively understand something: corrosion = thinning expansions = getting fat
        dilate = cv2.dilate(erode, kernel, 3)

        # Closed operations
        close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)  # cv2.morphologyEx() Perform various morphological changes
        close = cv2.morphologyEx(close, cv2.MORPH_CLOSE, kernel)

        # cv2.findContours ()Find the outline of the detection object.
        contours, h = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )

        # draw a line
        # cv2.line(image, start_point, end_point, color, thickness)
        # cv2.line(frame, (20, 500), (1300, 550), (0, 255, 255), 3)

        for (i, c) in enumerate(contours):  # enumerate()Data Objects Traversed
            (x, y, w, h) = cv2.boundingRect(c)  # cv2.boundingRect()This function gets some information about the minimum rectangular border of an image

            # Filter small test box
            isshow = (w >= 90) and (h >= 90)
            if not isshow:
                continue

            # Save Hub information
            # cv2.rectangle include： (img, pt1, pt2, color, thickness=None, lineType=None, shift=None)
            # cv2.rectangle(Read the picture variable, (top left) (bottom right), (color), (line width)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            centre_p = (x + int(w / 2), y + int(h / 2))
            cars.append(centre_p)

            # cv2.circle(frame, centre_p, 5, (0, 0, 255), -1)
            for (x, y) in cars:
                if 593 < y < 607:
                    car_n += 1
                    cars.remove((x, y))

    # cv2.putText(img，text，org, fontFace, fontScale, color, thinckness, lineType, bottomLeftOrigin)
    # cv2.putText(Pictures, text displayed, detection box upper left corner coordinates, fonts, font size, color, bold font)
    cv2.putText(frame, "Cars Count:" + str(car_n), (500, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:  # Esc
        break

cap.release()
cv2.destroyAllWindows()
