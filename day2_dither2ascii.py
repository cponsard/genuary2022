"""
Genuary2022 Day 2 Dithering
Dithering to Ascii Art by C. Ponsard
Free under the terms of GPLv3 license

Run and open day2_wishes.txt file in texteditor or word processor
Using C64 Pro Mono (square char) gives a good and contrasted rendering (see day2_wishes.docx)
Alternately can only use even line number by changer range(hauteur) to range(0,hauteur,2)

Requires Pillow (PIL)
"""

from PIL import Image
import io

def main():
    image_path = "day2_wishes.png"
    image = Image.open(image_path)
    largeur, hauteur = image.size
    output = io.StringIO()
    image_grey = image.convert('L')

    sel = 0
    err = 0
    for y in range(hauteur):
        for x in range(largeur):
            value = (image_grey.getpixel((x, y))+image_grey.getpixel((x, y)))//2
            if value < 28:
                output.write('@')
            elif value < 56:
                output.write('%')
            elif value < 84:
                output.write('#')
            elif value < 112:
                output.write('*')
            elif value < 140:
                output.write('+')
            elif value < 168:
                output.write('=')
            elif value < 196:
                output.write('-')
            elif value < 224:
                output.write(':')
            else:
                output.write('.')
        output.write('\n')

    with open('day2_wishes.txt', mode='w') as f:
        print(output.getvalue(), file=f)

    # webbrowser.open('day2_wishes.txt') # requires additional library

if __name__ == '__main__':
    main()