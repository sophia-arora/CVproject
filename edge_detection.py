import cv2
import numpy as np

def apply_gaussian_blur(image, kernel_size=(5, 5), sigma_x=0):
    """Apply Gaussian blur to an image."""
    return cv2.GaussianBlur(image, kernel_size, sigma_x)

def sobel_edge_detection(image, scale=1, delta=0, ddepth=cv2.CV_16S):
    """Perform Sobel edge detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    return cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

def laplacian_edge_detection(image, ddepth=cv2.CV_16S):
    """Perform Laplacian edge detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, ddepth)

# Load your image (make sure to provide the correct path to your image file)
image_path = 'path_to_your_image.jpg'
image = cv2.imread(image_path)

# Apply Gaussian Blur
blurred_image = apply_gaussian_blur(image)

# Perform Sobel edge detection
sobel_edges = sobel_edge_detection(blurred_image)

# Perform Laplacian edge detection
laplacian_edges = laplacian_edge_detection(blurred_image)

# Display results
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred_image)
cv2.imshow('Sobel Edge Detection', sobel_edges)
cv2.imshow('Laplacian Edge Detection', laplacian_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
