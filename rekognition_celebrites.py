import boto3
from pathlib import Path
from PIL import Image,ImageDraw

client = boto3.client('rekognition')
image_path = str(Path(__file__).parent / "images"/"images.jpg")

def get_celebrity(image_path):
    with open(image_path,"rb") as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})
    return response

def get_rectangle(target_path,response):
    image = Image.open(target_path)
    draw = ImageDraw.Draw(image)

    width,height = image.size

    for celebrity in response["CelebrityFaces"]:
        box = celebrity["Face"]["BoundingBox"]
        left = int(box["Left"] * width)
        top = int(box["Top"] * height)
        right = int((box["Left"] + box["Width"]) * width)
        bottom = int((box["Top"] + box["Height"]) * height)

        draw.rectangle([left,top,right,bottom],outline="red",width=3)
        draw.text((left,top-10),text=f"{celebrity["Name"]}",fill="red")

    image.show()

if __name__ == "__main__":
    response = get_celebrity(image_path)
    get_rectangle(image_path,response)


