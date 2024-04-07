from ultralytics import YOLO
import streamlit as st
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as PLImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from email_feature import *

def draw_boxes(image, boxes):
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=2)
    return image

img = st.camera_input("Upload Image")
recipent_email = st.text_input("Enter a valid email address: ")
upload = st.button('Upload')

if upload:
    img = Image.open(img)
    img.save('temp_file.jpg')
    st.image(img, caption='Uploaded Image', use_column_width=True)

    model = YOLO('best.pt').load('best.pt')
    model.cpu()
    results = model('temp_file.jpg')

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        st.write(boxes)
        names = result.names
        classes = result.boxes.cls.cpu().numpy()
        st.info(f'Fracture Found in {names[classes[0]]}')

    img_with_boxes = draw_boxes(img.copy(), boxes)
    st.image(img_with_boxes, caption='Image with Bounding Boxes', use_column_width=True)


    page_width, page_height = letter
    img_width, img_height = img_with_boxes.size
    if img_width > page_width or img_height > page_height:
        ratio = min(page_width / img_width, page_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        img_with_boxes = img_with_boxes.resize((new_width, new_height), Image.Resampling.BICUBIC)

    img_with_boxes.save('temp_with_boxes.jpg')

    doc = SimpleDocTemplate("report.pdf", pagesize=letter)
    content = []


    title_style = ParagraphStyle(name='Title', fontSize=20, alignment=1, spaceAfter=20)
    title = Paragraph("<b>Waste Report</b>", title_style)
    content.append(title)

 
    detection_message = (f"We found a  waste {names[classes[0]]}. "
                         "Please note that although we use advanced AI algorithms, "
                         "we do not provide 100% certainty of the detection. We advise "
                        )
    detection_message_style = ParagraphStyle(name='DetectionMessage', fontSize=12, spaceAfter=20)
    detection_message_paragraph = Paragraph(detection_message, detection_message_style)
    content.append(detection_message_paragraph)
    content.append(PLImage("temp_with_boxes.jpg", width=250, height=250))

    doc.build(content)
    st.success("PDF report generated successfully!")
    if len(recipent_email) > 5:
        subject = "Plastic waste report"
        message = "Please find attached the waste report."
        pdf_path = "report.pdf"
        send_email(recipent_email, subject, message, pdf_path)
        st.success("Email Sent Successfully")