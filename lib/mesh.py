from PIL import Image
import numpy as np

def save_as_obj(image, depthmap):
    height, width, channels = image.shape
    file = open("object.obj", "w")

    # name 
    file.write("o 3D image\n")
    file.write("\n")

    # vertices 
    for i in range(height):
        for j in range(width):
            x, y, z = j, 255-i, 255*depthmap[i,j]
            coord = (x, y, z)
            color = image[i,j]
            coord = str(coord[0])+" "+str(coord[1])+" "+str(coord[2])
            color = str(color[0])+" "+str(color[1])+" "+str(color[2]) # UNUSED
            file.write("v "+coord+"\n")
    file.write("\n")

    # vertices texture coordinate
    #file.write("vt 0.0 0.0 0.0\n") # (unused for now)
    #file.write("\n")

    # vertices normals
    #file.write("vn 0.0 0.0 0.0\n") # (unused for now)
    #file.write("\n")

    # faces
    for i in range(height):
        for j in range(width):
            coord = i*width + j +1

            # even lines
            if i%2 == 0:
                # has valid neighbours
                if i+1<height and j+1<width:
                    right_neighbour = i*width + (j+1) +1
                    bottom_neighbour = (i+1)*width + j +1
                    file.write("f "+str(coord)+"// "+str(right_neighbour)+"// "+str(bottom_neighbour)+"//\n")
            # odd lines
            else :
                # has valid neighbours
                if i-1>0 and j-1>0:
                    left_neighbour = i*width + (j-1) +1
                    top_neighbour = (i-1)*width + j +1
                    file.write("f "+str(coord)+"// "+str(left_neighbour)+"// "+str(top_neighbour)+"//\n")
    file.write("\n")

    return None
