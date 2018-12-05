import numpy as np
import matplotlib.pyplot as plt
import cv2

#Filtros
sobel_x = np.array([[-1, 0, 1], 
                    [-2, 0, 2], 
                    [-1, 0, 1]])

sobel_y = np.array([[-1, -2, -1], 
                    [0, 0, 0], 
                    [1, 2, 1]])
                
gaussian_blur = (1 / 16) * np.array([[1, 2, 1], 
                                     [2, 4, 2], 
                                     [1, 2, 1]])

#Lendo a imagem
img = cv2.imread("Imagem.jpg", cv2.IMREAD_GRAYSCALE)
#Caso a imagem seja muito grande, reduzir qualidade para acelerar processo
if len(img) > 1000:
    img = cv2.resize(img, (int(img.shape[1] / 5), int(img.shape[0] / 5)))
img = np.asarray(img) 

#Convoluções (aplicando filtros)
def convolution(img, kernel):
    output_height = img.shape[0] - len(kernel) + 1
    output_width =  img.shape[1] - len(kernel) + 1
    convolutions = []
    for step_down in range(output_height):
        for step_right in range(output_width):
            step_results = []
            for row in range(len(kernel)):
                for column in range(len(kernel)):
                    step_result = kernel[row][column] * img[row + step_down][column + step_right]
                    step_results.append(step_result)
            convolutions.append(sum(step_results))
    return np.asarray(convolutions).reshape((output_height, output_width))
    
def sobel(img, kernel_x, kernel_y):
    img_x = convolution(img, kernel_x)
    img_y = convolution(img, kernel_y)
    new_img = np.sqrt(np.square(img_x) + np.square(img_y))
    return new_img

blur_img = convolution(img, gaussian_blur)
sobel_blur_img = sobel(blur_img, sobel_x, sobel_y)
sobel_img = sobel(img, sobel_x, sobel_y)

#Plotando resultados
plt.figure(figsize = (18, 6))
plt.subplot(1, 3, 1)
plt.imshow(img, cmap = "gray")
plt.title("Original")
plt.subplot(1, 3, 2)
plt.imshow(sobel_img, cmap = "gray")
plt.title("Sobel Edge Detection without Gaussian Blur")
plt.subplot(1, 3, 3)
plt.imshow(sobel_blur_img, cmap = "gray")
plt.title("Sobel Edge Detection with Gaussian Blur")