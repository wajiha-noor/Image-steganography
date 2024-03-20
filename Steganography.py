from PIL import Image
import cv2
import numpy as np
from bitstring import BitArray 

def hide_and_extract(secret_path, cover_path):
    secret_image = cv2.imread(secret_path)
    cover_image = cv2.imread(cover_path)
    if secret_image.size != cover_image.size:
        print("Both images must have same resolution")
        return
    combined_image = cover_image.copy()
    for x in range(cover_image.shape[1]):
        for y in range(cover_image.shape[0]):
            for c in range(3): 
                cover_pixel = cover_image[y, x, c]
                secret_pixel = secret_image[y, x, c]
                cover_bin_pixel = np.binary_repr(cover_pixel,width=8)
                secret_bin_pixel = np.binary_repr(secret_pixel,width=8)
                new_pixel = cover_bin_pixel[0:4]+secret_bin_pixel[0:4]
                combined_image[y, x, c] = BitArray(bin=new_pixel).uint8

    cv2.imwrite("combined_image.png", combined_image)

    extracted_image = combined_image.copy()
    for x in range(combined_image.shape[1]):
        for y in range(combined_image.shape[0]):
            for c in range(3): 
                bin_val = np.binary_repr(combined_image[y,x,c],width=8)
                pixel_val = BitArray(bin= (bin_val[4:8]+'0000')).uint8
                extracted_image[y, x, c] = pixel_val

    cv2.imwrite("extracted_image.png", extracted_image)

    while True:
        user_choice = input("Press 1 to see Secret Image\n2 to see Cover Image\n3 to see Combined Image\n4 to see Extracted Image\n'q' to quit: ")
        if user_choice.lower() == 'q':
            break
        elif user_choice == '1':
            cv2.imshow('Cover Image', secret_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif user_choice == '2':
            cv2.imshow('Secret Image', cover_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif user_choice == '3':
            cv2.imshow('Combined Image', combined_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif user_choice == '4':
            cv2.imshow('Extracted Image', extracted_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 'q'.")

#Images Must be of Same Size
secret_image_path = "(ADD PATH OF IMAGE TO HIDE)"
cover_image_path = "(ADD PATH OF DISPLAY IMAGE)"

hide_and_extract(secret_image_path, cover_image_path)

