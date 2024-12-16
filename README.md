# Air Hockey
#### Video Demo: https://youtu.be/-UAmQHcnM4A
#### Description:

My final project for the Python course is called Air Hockey. It's a software representation of the Air Hockey game.

In my early years I was very into gaming and my dream was to create a game of my own someday. Luckily, CS50 gave me that chance.

I decided to use 'pygame' to make the game. I chose it since it's one of the most popular libraries for developing games in Python and it has rich functionality to abstract some of the physics aspects.

I created 3 more functions in addition to 'main'. 'Collision' takes the position of a puck and both sticks to calculate the direction vector of a puck after collision with a stick. The 'stick_v' function is used to calculate the velocity of a stick. It detects the stick and calculates its velocity for smooth movement and for further puck velocity calculation in the next function. The 'puck_v' function takes stick velocity and calculates puck velocity based on stick velocity after collision.

Within the 'main' function I have some predefined variables. Then I used pygame functions to draw the background, a puck, both sticks and borders of the table. Almost all objects are rectangles that use Rect class-related methods to program their behavior. There's a while loop that loops the program and re-draws all objects. FPS is 60. In order to correctly check for border collisions with the puck, I had to create borders, and then check whether the puck hit them. But, for some reason, the puck could've gone through the border and gotten stuck. So, I decided to draw the puck inside another rectangle that represented the background (air hockey table) and it worked. In order to change the puck direction after collision I just give the puck a negative vector for both coordinates x and y (the opposite of what it was before the collision). Friction for the puck is added to make it slow down gradually. 'colliderect' pygame function captures multiple collisions even if objects hit each other only once (visually at least). So, I had to make a workaround and add 's' variable that gets initialized with 1 if collision is detected. In this way, I'll always add only 1 to the score, even if 'colliderect' contains multiple collisions.

The biggest challenge was the calculation of vectors, making the puck move smoothly and hit the borders correctly, making pucks move as expected. I understand that the code base is a bit chaotic. It was possible to use classes and structure the code more efficiently, but I decided to leave some space for improvements once I gained more knowledge and experience.


