import cv2 
import numpy as np 


"""def dist(point1, point2):
    return abs((point1[0]**2-point2[0]**2) - (point1[1]**2-point2[1]**2))"""



img = cv2.imread('website_project/maroon5.jpg', cv2.IMREAD_COLOR) 


gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 


gray_blurred = cv2.blur(gray, (7, 7)) 


detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1.1, 40, param1 = 50, 
               param2 = 70, minRadius = 50, maxRadius = 1000) 
  

if detected_circles is not None: 
    main_circle = (0, 0, 0)

    detected_circles = np.uint16(np.around(detected_circles)) 

    for pt in detected_circles[0, :]: 
        (a, b, r) = (pt[0], pt[1], pt[2])

        if r >= main_circle[2]:
            main_circle = (a, b, r)


    cv2.circle(img, (main_circle[0], main_circle[1]), main_circle[2], (0, 255, 0), 2) 

    cv2.circle(img, (main_circle[0], main_circle[1]), 1, (0, 0, 255), 3) 

    cv2.imshow("Detected Circle", img) 
    cv2.waitKey(0) 
    cv2.destroyAllWindows()


