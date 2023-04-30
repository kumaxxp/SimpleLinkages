#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Linkages_lib.FiveBarLinkage as FiveBarLinkage
import Linkages_lib.FourBarSubLinkage as FourBarSubLinkage
import Linkages_2d.linkage_2d_five as linkage_2d_five
import Linkages_lib.CulcLinkage as lculc


import pygame

# Initialize pygame
pygame.init()

# Set the width and height of the screen (width, height)
screen_size = (800, 600) 
screen = pygame.display.set_mode(screen_size)

# Set the title of the window
pygame.display.set_caption("Linkage Simulation")

# Loop until the user clicks the close button or press Alt+F4 or press ESC
done = False

# Manage how fast the screen updates
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Define button properties
button_width = 150
button_height = 40
button_margin = 10

# Create mode buttons as Rect objects
mode1_button = pygame.Rect(button_margin, button_margin, button_width, button_height)
mode2_button = pygame.Rect(button_margin * 2 + button_width, button_margin, button_width, button_height)
mode3_button = pygame.Rect(button_margin * 3 + button_width * 2, button_margin, button_width, button_height)

# Set the initial mode
current_mode = 1

def draw_button(screen, button_rect, text, bg_color, fg_color):
    """Draw a button on the screen."""
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, fg_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, bg_color, button_rect)
    screen.blit(text_surface, text_rect)

# Define slider properties
slider_width = 200
slider_height = 20
thumb_radius = 12

# Initialize slider values
slider1_value = 50
slider2_value = 50

# Create slider Rect objects
slider1_rect = pygame.Rect(100, 100, slider_width, slider_height)
slider2_rect = pygame.Rect(100, 150, slider_width, slider_height)

# Clamp the slider values to their respective ranges
def clamp_slider_value(value, min_val=0, max_val=100):
    return min(max_val, max(min_val, value))

def draw_slider(screen, slider_rect, thumb_pos):
    """Draw a slider on the screen."""
    # Draw the slider bar
    pygame.draw.rect(screen, GRAY, slider_rect)
    
    # Draw the slider thumb
    thumb_x = slider_rect.x + thumb_pos
    thumb_y = slider_rect.y + slider_rect.height // 2
    pygame.draw.circle(screen, WHITE, (thumb_x, thumb_y), thumb_radius)

# Update the handle_mouse_event function to handle slider dragging
dragging_slider1 = False
dragging_slider2 = False

def handle_mouse_event(event):
    global current_mode, dragging_slider1, dragging_slider2
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button clicked
            if mode1_button.collidepoint(event.pos):
                current_mode = 1
            elif mode2_button.collidepoint(event.pos):
                current_mode = 2
            elif mode3_button.collidepoint(event.pos):
                current_mode = 3
            elif slider1_rect.collidepoint(event.pos) and current_mode == 2:
                dragging_slider1 = True
            elif slider2_rect.collidepoint(event.pos) and current_mode == 2:
                dragging_slider2 = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  # Left mouse button released
            dragging_slider1 = False
            dragging_slider2 = False

class Robot:
    def __init__(self):
        # Initialization of robot parameters, e.g., joint angles, link lengths, etc.
        pass
    
    def auto_inverse_kinematics(self, target_position):
        # Reuse the original code of auto_inverse_kinematics function and make necessary changes
        # to adapt it to the class structure
        
        # Perform the inverse kinematics calculations
        
        # Return the joint angles or any desired output
        #return joint_angles
        pass
    
# Create a robot instance
my_robot = Robot()

# -------- Main Program Loop -----------
while not done:
    # Clear the screen
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        else:
            handle_mouse_event(event)

    # --- Draw buttons
    # Render the button text using the Japanese font
    draw_button(screen, mode1_button, "Auto Inverse", LIGHT_GRAY, GRAY)
    draw_button(screen, mode2_button, "Manual Inverse", LIGHT_GRAY, GRAY)
    draw_button(screen, mode3_button, "Manual Forward", LIGHT_GRAY, GRAY)

    # Update sliders when they are being dragged
    if dragging_slider1:
        slider1_value = ((pygame.mouse.get_pos()[0] - slider1_rect.x) / slider_width) * 100
        slider1_value = clamp_slider_value(slider1_value)
    if dragging_slider2:
        slider2_value = ((pygame.mouse.get_pos()[0] - slider2_rect.x) / slider_width) * 100
        slider2_value = clamp_slider_value(slider2_value)

    # Draw the sliders when in Mode 2
    if current_mode == 2:
        draw_slider(screen, slider1_rect, int(slider1_value / 100 * slider_width))
        draw_slider(screen, slider2_rect, int(slider2_value / 100 * slider_width))


    if current_mode == 1:   # Auto mode for elliptical movement with inverse kinematics
        t_step = 0
        while True:
            t_step = my_robot.auto_inverse_kinematics(t_step)


    # - Update the screen
    pygame.display.flip()

    # - Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit
pygame.quit()


