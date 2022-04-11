from PIL import Image
import argparse
import os
import numpy as np
def main():
    parser = argparse.ArgumentParser("Imto16bit")
    parser.add_argument("--input","-I",required=True)
    parser.add_argument("--output","-O")
    args = parser.parse_args()
    if(args.input and os.path.isfile(args.input)):
        fname = args.input
        print("Converting image to 128x128")
        img = Image.open(fname)
        nimg = np.array(img.resize((128,128)).convert("RGB"))
        n16 = np.array(np.zeros((128,128)),dtype=np.uint16)
        n16 = ((nimg[:,:,0].astype(np.uint16) & 0xF8) << 8)  |   ((nimg[:,:,1].astype(np.uint16) & 0xFC) << 3)   |   ((nimg[:,:,2].astype(np.uint16) & 0xF8) >> 3)
        n16 = ((n16 & 0xFF00) >> 8) | ((n16 & 0xFF) << 8)

        MASK5 = 0b011111
        MASK6 = 0b111111

        # TODO: BGR or RGB? Who knows!
        b = (n16 & MASK5) << 3
        g = ((n16 >> 5) & MASK6) << 2
        r = ((n16 >> (5 + 6)) & MASK5) << 3
        
        # Compose into one 3-dimensional matrix of 8-bit integers
        rgb = np.dstack((r,g,b)).astype(np.uint8)
        img = Image.fromarray(rgb,"RGB")
        img.show()
        code = "#ifdef ST7735_IS_128X128\nconst uint16_t test_img_128x128[][128] = %s;\n#endif\n"%(
            "{\n%s}"%(",\n".join(["{%s}"%(",".join([["0x%04X"%(n16[y,127-x]) for x in range(0,128)] for y in range(0,128)][i])) for i in range(0,128)]))
        )
        with open(args.output if args.output else "img.h","w") as fp:
            fp.write(code)
    else:
        print("Please enter valid file path")



if __name__ == "__main__":
    main()