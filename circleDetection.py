import cv2 
import numpy as np 


"""def dist(point1, point2):
    return abs((point1[0]**2-point2[0]**2) - (point1[1]**2-point2[1]**2))"""




def circleDetect(img):
    # Read circle detection image
    img = cv2.imread(img, cv2.IMREAD_COLOR) 

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 

    # Blur to accentuate circle in can, by basically removing background through intense blur
    gray_blurred = cv2.blur(gray, (7, 7)) 

    # Detects all possible circles in image
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1.1, 40, param1 = 50, 
                param2 = 70, minRadius = 50, maxRadius = 1000) 
    
    # Verifies that circles exist in image
    if detected_circles is not None: 
        main_circle = (0, 0, 0)

        detected_circles = np.uint16(np.around(detected_circles)) 

        # Checks for circle that exist on the can you are detecting from, and then takes the largest one (outer rim)
        for pt in detected_circles[0, :]: 
            (a, b, r) = (pt[0], pt[1], pt[2])

            if r >= main_circle[2]:
                main_circle = (a, b, r)

        # Places circle on the image
        cv2.circle(img, (main_circle[0], main_circle[1]), main_circle[2], (0, 255, 0), 2) 

        cv2.circle(img, (main_circle[0], main_circle[1]), 1, (0, 0, 255), 3) 

        # Shows image and wait for user to close it
        cv2.imshow("Detected Circle", img) 
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

# Fetches image that will be used in circle detection
image = "website-project/maroon5.jpg"
circleDetect(image)
