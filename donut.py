import math
import os
import pygame
import time

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("14. Archimedes.mp3")
    pygame.mixer.music.play(loops=-1)


def generate_torus_frame(a, b):
    width, height = 80, 40
    R1, R2 = 1, 2  # Radius of the torus
    K1, K2 = 25, 5 # Scaling factors

    output = [[" " for _ in range(width)] for _ in range(height)]
    zbuffer = [[0 for _ in range(width)] for _ in range(height)]

    # Shading characters
    shading = ["@", "#", "8", "&", "o", ":", "*", ".", "t", " "]

    for theta in range(0, 628, 7):
        for phi in range(0, 628, 2):
            theta_rad, phi_rad = theta / 100, phi / 100
            cos_theta, sin_theta = math.cos(theta_rad), math.sin(theta_rad)
            cos_phi, sin_phi = math.cos(phi_rad), math.sin(phi_rad)
            cos_a, sin_a = math.cos(a), math.sin(a)
            cos_b, sin_b = math.cos(b), math.sin(b)

            circle_x = R2 + R1 * cos_theta
            circle_y = R1 * sin_theta

            x = circle_x * (cos_b * cos_phi + sin_a * sin_b * sin_phi) - circle_y * cos_a * sin_b
            y = circle_x * (sin_b * cos_phi - sin_a * cos_b * sin_phi) + circle_y * cos_a * cos_b
            z = K2 + cos_a * circle_x * sin_phi + circle_y * sin_a
            ooz = 1 / z

            xp = int(width / 2 + K1 * ooz * x)
            yp = int(height / 2 - K1 * ooz * y)

            luminance = cos_phi * cos_theta * sin_b - cos_a * cos_theta * sin_phi - sin_a * sin_theta + cos_b * (cos_a * sin_theta - cos_theta * sin_a * sin_phi)

            luminance = max(-1, min (1, luminance))

            if 0 <= xp < width and 0 <= yp < height:
                if ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    # depth shading
                    char_index = int((luminance + 1) * (len(shading) - 1) / 2)
                    output[yp][xp] = shading[char_index]

    return "\n".join("".join(row) for row in output)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    play_music()
    a, b = 0, 0
    speed_factor = 1.10  # Initial speed of rotation
    try:
        while True:
            print("\033[H", end="")
            frame = generate_torus_frame(a, b)
            print(frame)

            # Gradually increase speed without going overboard
            a += speed_factor
            b += speed_factor / 2  # Slightly different speed for smoother rotation
            speed_factor *= 2.01  # make higher = brrrrrrrrr
            
            if speed_factor > 0.1:
                speed_factor = 0.1

            time.sleep(0.00)
    except KeyboardInterrupt:
        print("\nExited!")

if __name__ == "__main__":
    main()