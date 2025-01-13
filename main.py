import cv2
import numpy as np


# Read image
try:
       cap = cv2.VideoCapture(0)
except Exception:
       print("video could not be found")


slopes = []
MIN_DISTANCE=50
while True:
       ret, frame = cap.read()
       if not ret:
               print("failed to capture frame")
               break


       gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

       gaussian = cv2.GaussianBlur(gray, (5, 5), 0)

       edges = cv2.Canny(gaussian,50,150,apertureSize=3)

       output = frame.copy()
       
       height, width = frame.shape[:2]
       vertices = np.array([[(width // 4, height // 2), (3 * width // 4, height // 2),
                             (3* width // 4,  height), (width // 4, height)]], dtype=np.int32)
       mask = np.zeros_like(edges)
       cv2.fillPoly(mask, vertices, (255, 255, 255))
       masked_image = cv2.bitwise_and(edges, mask)
       lines = cv2.HoughLinesP(
                   masked_image,
                   1, 
                   np.pi/180,
                   threshold=50, 
                   minLineLength=15, 
                   maxLineGap=100 
                   )
       cv2.polylines(output, vertices, True, (0, 0, 255), 3)


       first_lane_lines = []
       second_lane_lines = []
     

       if lines is not None:
        for points in lines:
            print(len(lines))
            x1, y1, x2, y2 = points[0]

            slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 0

            
            if slope > 0:  
                second_lane_lines.append([(x1, y1), (x2, y2), slope])

            elif slope < 0:
                first_lane_lines.append([(x1, y1), (x2, y2), slope])

                
       if len(first_lane_lines) > 0 and len(second_lane_lines) > 0:
            avg_r_slope = 0
            avg_l_slope = 0
            l_slope_weight = 0
            r_slope_weight = 0
            left_point = ()
            right_point = ()
            """FORMULAS
            line is y=mx +b
            y intercept is y-mx
            points for line drawing is the line (y=mx+b) for both left and right intersections with y=height and y=height//2
            ^^ only if this is vertical
            otherwise with 
            """
            try:
                for n in range(len(first_lane_lines)):
                        slope = first_lane_lines[n][2]
                        if avg_l_slope == 0:
                            avg_l_slope = slope
                        elif 0.9 <= avg_l_slope/slope <= 1.1:
                            l_slope_weight += 1
                            avg_l_slope = (l_slope_weight*avg_l_slope + slope)/(l_slope_weight+1)
                            left_point = first_lane_lines[n]

                l_y_int = np.float64(left_point[0][1])-avg_l_slope*np.float64(left_point[0][0])
                if abs(avg_l_slope)>0.75:
                    first_x1 = (np.float64(height)-l_y_int)/avg_l_slope
                    first_y1 = np.float64(height)
                    first_x2 = (np.float64(height)-2*l_y_int)/(2*avg_l_slope)
                    first_y2 = np.float64(height/2)

                else:
                    first_x1 = np.float64(width/4)
                    first_y1 = (4*l_y_int+avg_l_slope*np.float64(width))/4
                    first_x2 = np.float64(3*width/4)
                    first_y2 = (4*l_y_int+avg_l_slope*3*np.float64(width))/4

            except Exception:
                print(Exception)
            

            try:
                for n in range(len(second_lane_lines)):
                        slope = second_lane_lines[n][2]
                        if avg_r_slope == 0:
                            avg_r_slope = slope
                        elif 0.9 <= avg_r_slope/slope <= 1.1:
                            r_slope_weight += 1
                            avg_r_slope = (r_slope_weight*avg_r_slope + slope)/(r_slope_weight+1)
                            right_point = second_lane_lines[n]

                r_y_int = np.float64(right_point[0][1])-avg_r_slope*np.float64(right_point[0][0])
                if abs(avg_r_slope)>0.75:
                    second_x1 = (np.float64(height)-r_y_int)/avg_r_slope
                    second_y1 = np.float64(height)
                    second_x2 = (np.float64(height)-2*r_y_int)/(2*avg_r_slope)
                    second_y2 = np.float64(height/2)
                else:
                    second_x1 = np.float64(width/4)
                    second_y1 = (4*r_y_int+avg_r_slope*np.float64(width))/4
                    second_x2 = np.float64(3*width/4)
                    second_y2 = (4*r_y_int+avg_r_slope*3*np.float64(width))/4

            except Exception:
                print(Exception)
            
            # lines in form y = mx + b || m is left/right slope || b find with intersection with frame boundaries
            try:

                first_point1 = tuple(np.round(np.array([first_x1, first_y1], dtype=np.float64)).astype(np.int32))
                first_point2 = tuple(np.round(np.array([first_x2, first_y2], dtype=np.float64)).astype(np.int32))
                second_point1 = tuple(np.round(np.array([second_x1, second_y1], dtype=np.float64)).astype(np.int32))
                second_point2 = tuple(np.round(np.array([second_x2, second_y2], dtype=np.float64)).astype(np.int32))

                cv2.line(output, first_point1, first_point2, (0, 255, 0), 2)
                cv2.line(output, second_point1, second_point2, (0, 255, 0), 2)

                print(first_point2[0])
                center_x1 = (first_point1[0]+second_point1[0])//2
                center_y1 = (first_point1[1]+second_point1[1])//2
                center_x2 = (first_point2[0]+second_point2[0])//2
                center_y2 = (first_point2[1]+second_point2[1])//2

                cv2.line(output, (center_x1, center_y1), (center_x2, center_y2), (0, 0, 255), 4)
            except Exception:
                print(Exception)


       cv2.imshow('Detected Lines and Centerline', output)


       if cv2.waitKey(1) & 0xFF == ord('q'):
                break


cap.release()
cv2.destroyAllWindows()
