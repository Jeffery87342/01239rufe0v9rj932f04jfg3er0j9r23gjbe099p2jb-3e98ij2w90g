#!/usr/bin/env python3
"""
FunCaptcha Image Processing Utilities
Provides image analysis and processing functions for solving FunCaptcha challenges.
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2
from typing import Tuple, List


class ImageProcessor:
    """Utility class for processing FunCaptcha challenge images."""
    
    @staticmethod
    def preprocess_image(image: Image.Image) -> np.ndarray:
        """
        Preprocess an image for analysis.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed numpy array
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance image
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        return img_array
    
    @staticmethod
    def detect_edges(image: Image.Image) -> np.ndarray:
        """
        Detect edges in an image using Canny edge detection.
        
        Args:
            image: PIL Image object
            
        Returns:
            Edge-detected image as numpy array
        """
        img_array = np.array(image.convert('L'))  # Convert to grayscale
        
        # Apply Canny edge detection
        edges = cv2.Canny(img_array, 100, 200)
        
        return edges
    
    @staticmethod
    def calculate_rotation_angle(image: Image.Image) -> int:
        """
        Calculate the rotation angle needed to orient an image correctly.
        
        Args:
            image: PIL Image object
            
        Returns:
            Rotation angle in degrees
        """
        img_array = np.array(image.convert('L'))
        
        # Detect edges
        edges = cv2.Canny(img_array, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
        
        if lines is not None:
            angles = []
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta)
                angles.append(angle)
            
            # Find the most common angle
            if angles:
                median_angle = np.median(angles)
                
                # Normalize to 0, 90, 180, 270
                rotation = round(median_angle / 90) * 90
                return rotation % 360
        
        # Default to 0 if no lines detected
        return 0
    
    @staticmethod
    def calculate_similarity(image1: Image.Image, image2: Image.Image) -> float:
        """
        Calculate similarity between two images.
        
        Args:
            image1: First PIL Image
            image2: Second PIL Image
            
        Returns:
            Similarity score (0-1, where 1 is identical)
        """
        # Resize both images to same size
        size = (100, 100)
        img1 = image1.resize(size).convert('RGB')
        img2 = image2.resize(size).convert('RGB')
        
        # Convert to numpy arrays
        arr1 = np.array(img1).flatten()
        arr2 = np.array(img2).flatten()
        
        # Calculate correlation coefficient
        correlation = np.corrcoef(arr1, arr2)[0, 1]
        
        return max(0, correlation)
    
    @staticmethod
    def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """
        Extract dominant colors from an image.
        
        Args:
            image: PIL Image object
            num_colors: Number of dominant colors to extract
            
        Returns:
            List of RGB tuples representing dominant colors
        """
        # Resize image for faster processing
        img = image.resize((100, 100)).convert('RGB')
        img_array = np.array(img)
        
        # Reshape to list of pixels
        pixels = img_array.reshape(-1, 3)
        
        # Use k-means clustering to find dominant colors
        from sklearn.cluster import KMeans
        
        try:
            kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = kmeans.cluster_centers_.astype(int)
            return [tuple(color) for color in colors]
        except:
            # Fallback to simple method if sklearn not available
            unique_colors = np.unique(pixels, axis=0)
            return [tuple(color) for color in unique_colors[:num_colors]]
    
    @staticmethod
    def detect_objects(image: Image.Image) -> List[Tuple[int, int, int, int]]:
        """
        Detect objects/regions in an image using contour detection.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of bounding boxes (x, y, width, height)
        """
        img_array = np.array(image.convert('L'))
        
        # Apply threshold
        _, thresh = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        bounding_boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10 and h > 10:  # Filter small noise
                bounding_boxes.append((x, y, w, h))
        
        return bounding_boxes
    
    @staticmethod
    def calculate_image_features(image: Image.Image) -> dict:
        """
        Calculate various features of an image for classification.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary of image features
        """
        img_array = np.array(image.convert('RGB'))
        
        features = {
            'mean_brightness': np.mean(img_array),
            'std_brightness': np.std(img_array),
            'mean_red': np.mean(img_array[:, :, 0]),
            'mean_green': np.mean(img_array[:, :, 1]),
            'mean_blue': np.mean(img_array[:, :, 2]),
            'variance': np.var(img_array),
            'entropy': ImageProcessor._calculate_entropy(img_array),
        }
        
        return features
    
    @staticmethod
    def _calculate_entropy(img_array: np.ndarray) -> float:
        """Calculate entropy of an image (measure of randomness)."""
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        else:
            gray = img_array.astype(np.uint8)
        
        # Calculate histogram
        histogram, _ = np.histogram(gray, bins=256, range=(0, 256))
        
        # Normalize
        histogram = histogram / histogram.sum()
        
        # Calculate entropy
        entropy = -np.sum(histogram * np.log2(histogram + 1e-10))
        
        return entropy


class ChallengeSolver:
    """Specialized solvers for different FunCaptcha challenge types."""
    
    @staticmethod
    def solve_rotation(image: Image.Image) -> int:
        """
        Solve a rotation challenge.
        
        Args:
            image: Challenge image
            
        Returns:
            Rotation angle in degrees
        """
        processor = ImageProcessor()
        
        # Try to detect rotation using edge detection
        angle = processor.calculate_rotation_angle(image)
        
        return angle
    
    @staticmethod
    def solve_dice_challenge(images: List[Image.Image]) -> List[int]:
        """
        Solve a dice counting challenge.
        
        Args:
            images: List of dice images
            
        Returns:
            List of dice counts
        """
        counts = []
        
        for image in images:
            # Detect dots/pips on the dice
            gray = np.array(image.convert('L'))
            
            # Use blob detection or contour counting
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Count significant contours as dots
            count = len([c for c in contours if cv2.contourArea(c) > 50])
            counts.append(min(count, 6))  # Dice have max 6 dots
        
        return counts
    
    @staticmethod
    def solve_animal_selection(images: List[Image.Image]) -> List[int]:
        """
        Solve an animal selection challenge.
        
        Args:
            images: List of images to classify
            
        Returns:
            List of indices containing animals
        """
        selected = []
        
        for idx, image in enumerate(images):
            features = ImageProcessor.calculate_image_features(image)
            
            # Simple heuristic for animal detection
            # Animals typically have medium variance and warm colors
            if features['variance'] > 1000 and features['mean_red'] > features['mean_blue']:
                selected.append(idx)
        
        return selected
