# Flappy Bird Game with Pygame

## Overview
This project is a simple implementation of the classic Flappy Bird game using the Pygame library. It serves as a practice project for beginners to learn the basics of game development with Pygame.

<div align="center" class="">
  <img src="assets\ss.png" alt="Flappy Bird Screenshot"/>
</div>

## Features
- **Player Controls:** Use the space bar to make the bird jump and avoid obstacles.
- **Obstacles:** Pipes appear at random intervals, and the player must navigate through them.
- **Score:** Keep track of score depending on playing time to challenge yourself and others.
- **Coin:** Keep track of the number of coins collected successfully passed to challenge 
yourself and others.

## Project Outcome
Along with the basics of pygame the major outcome of the project are:
- learned pygame surface rendering system
- learned pygame rectangle based collision system
- learned pygame feature : Group (pygame.sprite.Group)
- learned how to add audio in pygame

## Prerequisites
- Python 3.x
- Pygame library

## Installation
#### Use the pre-compiled exe file
   1. Download the zip by using the green code button
   2. Navigate to the windows/linux folder located in the app folder
   3. Run the .exe file

#### Useing the source code
1. Clone the repository :
   ```bash
   git clone https://github.com/FatinShadab/FlappyBird.git
   ```
2. Install the python requirements using pip:

   FOR WINDOWS
   ```bash
      pip install -r requirements.txt
   ```
   FOR LINUX
   ```bash
      pip3 install -r requirements.txt
   ```
3. Run the main.py file :

   FOR WINDOWS
   ```bash
      python main.py
   ```
   FOR LINUX
   ```bash
      python3 main.py
   ```

## Project Structure
- src/main.py: The main script containing the game logic.
- src/config.py: Configuration file for game settings.
- src/sprites.py: Module for defining game sprites and characters.

## Acknowledgments
### Inspiration
Flappy Bird game concept by Dong Nguyen.

This project was inspired by the tutorials and guidance provided by [Clear Code](https://www.youtube.com/@ClearCode). I followed their tutorials to understand the basics of game development with Pygame and incorporated my own features into the project.

I would like to express my gratitude to [Clear Code](https://www.youtube.com/@ClearCode) for their valuable content and educational resources.
