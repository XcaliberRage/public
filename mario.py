import cs50


def main():
    # get input
    while True:
        height = cs50.get_int("Height: ")

        if height > 0 and height < 9:
            break

    # Use the input to print the pyramid
    printPyramid(height)


def printPyramid(thisHeight):

    # get each row (counting 1 higher)
    for level in range(thisHeight):
        row = level + 1
        # Level defines how many blocks will appear in a row half
        printRow(row, thisHeight)


# Print the content of this row
def printRow(thisRow, maxWidth):

    # Print spaces equal to height - row
    for column in range(maxWidth - thisRow):
        print(" ", end="")

    # Print the number of blocks
    printBlocks(thisRow, "")
    # Print the space
    print("  ", end="")
    # Print the blocks again but new line after
    printBlocks(thisRow, "\n")

# Print blocks required for this half of the pyramid
def printBlocks(blockCount, ending):
    for block in range(blockCount):
        print("#", end="")
    print("", end=ending)


# Execute the main line
if __name__ == "__main__":
    main()