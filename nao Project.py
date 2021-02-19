# -*- encoding: UTF-8 -*- 
# This test demonstrates how to use the ALFaceDetection module.
# Note that you might not have this module depending on your distribution
#
# - We first instantiate a proxy to the ALFaceDetection module
#     Note that this module should be loaded on the robot's naoqi.
#     The module output its results in ALMemory in a variable
#     called "FaceDetected"

# - We then read this ALMemory value and check whether we get
#   interesting things.

import time
from PIL import Image
from naoqi import ALProxy

ip_address = "10.3.208.67"
port = 9559
leds = ALProxy("ALLeds", "10.3.208.67", 9559)


# ---------------------------------------------
def run():

  text2speech = ALProxy("ALTextToSpeech", ip_address, port)
  text2speech.say("") # work last when detect face, the AI speak

def show(naoImage):
  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]
  image_string = str(bytearray(array))

  # Create a PIL Image from our pixel array.
  im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

  # Save the image.
  im.save("camImage.png", "PNG")
  im.show()
  # Create a proxy to ALFaceDetection

try:
  faceProxy = ALProxy("ALFaceDetection", ip_address, port)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below

period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )

# ALMemory variable where the ALFacedetection modules
# outputs its results

memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", ip_address, port)
except Exception, e:
  print "Error when creating memory proxy:"
  print str(e)
  exit(1)


# A simple loop that reads the memValue and checks whether faces are detected.
for i in range(0, 20):
  time.sleep(0.5)
  val = memoryProxy.getData(memValue)

  print ""
  print "*****"
  print ""

  # Check whether we got a valid output.
  if(val and isinstance(val, list) and len(val) >= 2):

    # We detected faces !
    # For each face, we can read its shape info and ID.

    # First Field = TimeStamp.
    timeStamp = val[0]

    # Second Field = array of face_Info's.
    faceInfoArray = val[1]

    try:
      # Browse the faceInfoArray to get info on each detected face.
      for j in range( len(faceInfoArray)-1 ):
        faceInfo = faceInfoArray[j]

        # First Field = Shape info.
        faceShapeInfo = faceInfo[0]

        # Second Field = Extra info (empty for now).
        faceExtraInfo = faceInfo[1]

        print "  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
        print "  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])


        names = [
          "AllLedsBlue",
          "AllLedsGreen",
          "ChestLedsBlue",
          "ChestLedsGreen"]
        leds.createGroup("MyGroup", names)
        names = ["AllLeds"]
        leds.createGroup("MyGroup2", names)
        # Switch the new group on

        leds.on("MyGroup2")
        leds.off("MyGroup")

        motion = ALProxy("ALMotion", ip_address, port)
        text2speech = ALProxy("ALTextToSpeech", ip_address, port)
        text2speech.say("HEY YOU THERE")
        time.sleep(0.5)
        text2speech.say("STOP RIGHT THERE")
        motion.moveTo(0.5, 0, 0)  # move 1 meter forward
        text2speech = ALProxy("ALTextToSpeech", ip_address, port)
        text2speech.say("you need to wear a mask in this classroom")

        video_device = ALProxy("ALVideoDevice", ip_address, port)

        camera = 0  # CameraTop
        resolutions = 3  # k4VGA
        color_spaces = 13  # kBGRColorSpace
        fps = 1
        subscriber = video_device.subscribeCamera("demo1", camera, resolutions, color_spaces, fps)

        naoImage = video_device.getImageRemote(subscriber)

        show(naoImage)

        video_device.unsubscribe("demo1")

    except Exception, e:
      print "faces detected, but it seems getData is invalid. ALValue ="
      print val
      print "Error msg %s" % (str(e))
  else:
    print "No face detected"


    names = [
    "AllLedsBlue",
    "AllLedsRed"]
    leds.createGroup("MyGroup", names)
    names = [
    "AllLeds"]
    leds.createGroup("MyGroup2", names)
    # Switch the new group on
    leds.on("MyGroup2")
    leds.off("MyGroup")

    text2speech = ALProxy("ALTextToSpeech", ip_address, port)
    text2speech.say("THANK YOU FOR WEARING A MASK")




# Unsubscribe the module.
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."

if __name__ == '__main__':
    run()


