---
layout: page
title: Software
permalink: /software/
---
<br>
# Pairwise Stimuli Generator
-----------
*Loops through individual stimuli, pairs them up, and outputs to a separate folder on your local directory hierarchy*
<br><br>
<img src="/images/02b.png/" height=200px>
<br>

```python
def generateStims(left, right):

    """
    Left = Image on the left-hand side of the stimulus
    Right = Image on the right-hand side of the stimulus
    """

    border = (615,85,615,250)

    # Instantiate matplotlib object
    fig = plt.figure()

    # Left image
    ax1 = fig.add_subplot(1,1,1)
    face_l = Image.open(left)                        # Open and crop image from list
    face_l = ImageOps.crop(face_l, border)
    ax1.set_xticks([])                               # Format border (i.e., no tick marks!)
    ax1.set_yticks([])
    ax1.axis('off')
    plt.imshow(face_l)                               # Push image to matplotlib object

    # Right image
    ax2 = fig.add_subplot(1,2,2)
    face_r = Image.open(right)                       # Sim.
    face_r = ImageOps.crop(face_r, border)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.axis('off')
    plt.imshow(face_r)

    # Format and save to local directory
    fig.subplots_adjust(right=3)
    filename = "stim_{}_{}.png".format(left[7:14], right[7:14])
    fig.savefig(os.path.join(output, filename), bbox_inches="tight")
    plt.close()
```
<br> <br>

# Ensemble Array Generator
-----------

<br> <br>
<img src="/images/02a.png/">
<br> <br>

```python
def constructArray(hispanic, white, output):

    """
    Parameters
    Hispanic = Number of hispanic faces in the array
    White = Number of white faces in the array
    Output = Number of arrays that will be constructed
    There should be 12 total faces
    """
    counter = 1

    while (counter <= output):
        # Image Pool
        faces_H = np.random.choice(hispanicFaces, size = hispanic, replace = False).tolist()
        faces_W = np.random.choice(whiteFaces, size = white, replace = False).tolist()
        faces = faces_H + faces_W
        random.shuffle(faces)

        # Array Constructor
        w = 10
        h = 10
        fig = plt.figure(figsize=(13, 9))
        col = 4
        row = 3
        faceIndex = 0

        for i in range(1, (col*row)+1):
            border = (615,85,615,250)
            face = Image.open(faces[faceIndex])

            # NOTE: Cropping is optional here - this script is optimized for Chicago Face Database male images
            face = ImageOps.crop(face, border)
            ax = fig.add_subplot(row, col, i)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            plt.imshow(face)

            faceIndex += 1

        fig.subplots_adjust(wspace = -0.6, hspace= 0, )
        filename = str(hispanic).zfill(2) + "_" + str(white).zfill(2) + "_" + "faceArray" + str(counter).zfill(3)
        fig.savefig(os.path.join(path, filename))
        plt.close()
        sleep(1)
        counter += 1
```
