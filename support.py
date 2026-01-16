from csv import reader
import os
import pygame

def import_csv_layout(path):
    # Initializes an empty list to store the grid map data.
    terrain_map = []
    # Opens the CSV file located at the specified path.
    with open(path) as level_map:
        # Creates a CSV reader object to parse the file using a comma delimiter.
        layout = reader(level_map, delimiter=',')
        # Iterates over each row in the CSV file.
        for row in layout:
            # Converts the row to a list and appends it to the terrain map.
            terrain_map.append(list(row))
    # Returns the complete 2D list representing the map layout.
    return terrain_map

def import_folder(path):
    # Initializes an empty list to store loaded image surfaces.
    surface_list = []

    # Walks through the directory tree at the specified path.
    # We only care about the list of filenames (img_files) in the current directory.
    for _,__,img_files in os.walk(path):
        # Iterates through each file found in the directory.
        for image in img_files:
            # Constructs the full file path by joining the directory path and filename.
            full_path = os.path.join(path, image)
            # Loads the image from the disk and converts it for faster blitting with alpha transparency.
            image_surf = pygame.image.load(full_path).convert_alpha()
            # Adds the loaded surface to the list.
            surface_list.append(image_surf)
    # Returns the list containing all loaded images from the folder.
    return surface_list