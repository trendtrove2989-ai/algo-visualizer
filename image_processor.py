def scan_maze_secure(image_path):
    # 1. Check if image exists
    img = cv2.imread(image_path)
    if img is None: 
        return None, False # Failed
        
    # 2. Process for High-Contrast Maze Lines
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # We use a larger grid size here for better detail, or stay at COLS/ROWS
    # INTER_AREA is best for shrinking images without losing lines
    resized = cv2.resize(gray, (COLS, ROWS), interpolation=cv2.INTER_AREA)
    
    # Adaptive thresholding helps if the photo has shadows
    thresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Convert to our grid format (-1 for wall, 0 for path)
    new_grid = [[-1 if thresh[r, c] < 127 else 0 for c in range(COLS)] for r in range(ROWS)]
    
    return new_grid, True # Success