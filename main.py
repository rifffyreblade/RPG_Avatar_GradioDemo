import json
import requests
import os
import time
import datetime
import random
from PIL import Image

import gradio as gr

URL = "http://127.0.0.1:8188/prompt"
cancel_URL = "http://127.0.0.1:8188/interrupt"
INPUT_DIR = "E:/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/input/"
OUTPUT_DIR = "E:/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/output"


def get_latest_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image


def get_latest_video(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.gif'))]
    image_files = [f for f in image_files if f.lower().startswith('anim')]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image


def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)


def stop_queue():
    requests.post(cancel_URL)


def getStyle(style, prompt):
    styleStr = ""
    if style == "Hyper-Realistic Oil Painting":
        styleStr = "The Hyper-Realistic Oil Painting style is achieved through a blend of traditional techniques and modern digital tools. Artists often use programs like Corel Painter, Procreate, or Photoshop, equipped with custom brushes that mimic the texture and behavior of oil paints. Layers are built up using digital glazing techniques, with fine brushes used for intricate textures such as skin pores, fabric threads, or reflections on surfaces. Advanced color blending tools replicate the richness and subtlety of real oil paint. Lighting effects are crafted with high dynamic range (HDR) techniques, ensuring accurate highlights and shadows. For traditional mediums, artists use high-quality oil paints like Winsor & Newton, applied with soft bristle brushes and palette knives on a primed canvas. Varnishing adds a glossy finish, creating the illusion of depth and vibrancy. Whether digital or traditional, the process demands a meticulous eye for realism and an extraordinary level of patience."
    if style == "Anime/Manga":
        styleStr = "The Anime/Manga style relies on bold linework and expressive characters, crafted using tools such as Clip Studio Paint, Adobe Photoshop, or Procreate. Artists often use vector-based brushes to create smooth, consistent outlines and digital gradient tools to shade areas like hair and skin. Colors are vivid, with cel-shading techniques applied for sharp contrasts and clean edges. Backgrounds are often hand-drawn or digitally painted, blending soft brushes and gradient mapping for atmospheric depth. Motion and action scenes use speed lines, glowing effects, and particle brushes to heighten dynamism, while textures like halftone dots or screentones are added for a traditional manga feel. Layers are meticulously managed to separate characters, effects, and backgrounds for easy editing."
    if style == "Film Quality 3D Render":
        styleStr = "A Film-Quality 3D Render is achieved through industry-standard software such as Blender, Maya, or Cinema 4D, combined with rendering engines like V-Ray, Arnold, or Unreal Engine. Detailed modeling is created using polygonal or sculpting techniques, often with tools like ZBrush for high-resolution character or environment details. Textures are crafted in programs like Substance Painter or Mari, incorporating physically-based rendering (PBR) materials for realistic surface interaction with light. Lighting setups mimic cinematic techniques, using HDRI environments or custom lighting rigs for natural or dramatic effects. Final renders employ ray tracing for accurate reflections and shadows, with post-production enhancements in Adobe After Effects or Nuke for compositing and color grading."
    if style == "Live-Action Film Still":
        prompt["26"]["inputs"]["guidance"] = 2.5
        prompt["30"]["inputs"]["max_shit"] = 0.75
        prompt["30"]["inputs"]["base_shit"] = 0.5
        styleStr = "A Live-Action Film Still captures lifelike imagery, often using high-end cameras like the RED Digital Cinema or ARRI Alexa, paired with prime lenses to control depth of field and focus. On-set lighting techniques, such as three-point lighting or natural light diffused through softboxes, are key to creating the desired mood. Scene composition is informed by tools like the Golden Ratio or Rule of Thirds, while color grading software such as DaVinci Resolve enhances the aesthetic. In post-production, details are sharpened, noise is reduced, and additional effects like lens flares or film grain can be applied to add authenticity. Live-action film stills are framed with precision to evoke emotional impact and tell a visual story."
    if style == "Professional Photograph":
        prompt["26"]["inputs"]["guidance"] = 2.5
        prompt["30"]["inputs"]["max_shit"] = 0.75
        prompt["30"]["inputs"]["base_shit"] = 0.5
        styleStr = "A Professional Photograph relies on the precision and quality of equipment, such as a Canon EOS R5, Nikon Z9, or similar high-resolution cameras, paired with lenses suited to the subject (e.g., macro lenses for close-ups or wide-angle lenses for landscapes). Advanced lighting setups, including softboxes, reflectors, and strobes, control shadows and highlights. Post-processing in Adobe Lightroom or Photoshop refines the image, adjusting exposure, white balance, and sharpness. Details like skin retouching or background adjustments are handled with masking and cloning tools. Techniques such as HDR (High Dynamic Range) merging and focus stacking enhance clarity and depth, making every element crisp and visually striking."
    if style == "Amateur Photograph":
        prompt["26"]["inputs"]["guidance"] = 2.5
        prompt["30"]["inputs"]["max_shit"] = 0.75
        prompt["30"]["inputs"]["base_shit"] = 0.5
        styleStr = "An Amateur Photograph is defined by its unpolished and spontaneous quality, often taken with basic equipment like smartphones or entry-level cameras. These photos typically lack refined composition, with centered subjects, awkward angles, or cluttered backgrounds. Lighting is often uneven, leading to overexposed or underexposed areas, while focus and sharpness can be inconsistent. Post-processing, if present, is minimal or relies on basic filters, sometimes resulting in overediting. Amateur photographs capture authentic, candid moments but often overlook details such as framing, lighting, and thematic intent, giving them a raw, unrefined aesthetic."
    if style == "Realistic Cartoon":
        styleStr = "Creating a Realistic Cartoon involves a combination of stylized drawing and realistic rendering, often crafted in software like Adobe Illustrator, Photoshop, or 3D tools such as Blender or ZBrush. Characters are designed with exaggerated proportions, and their forms are shaded using techniques like gradient shading or ambient occlusion for depth. Textures, such as cloth or hair, are painted digitally using fine brushwork or imported as texture maps for additional realism. Dynamic lighting effects, like rim lighting or subsurface scattering (in 3D tools), give the cartoon characters a more lifelike feel. Environments use a mix of stylized assets and realistic details, often blending hand-drawn elements with digital enhancements for a polished look."
    return styleStr


def getTheme(style):
    styleStr = ""
    if style == "Dungeons & Dragons/Pathfinder":
        styleStr = "The Dungeons & Dragons/Pathfinder theme is centered on high fantasy, with narratives steeped in magic, heroism, and adventure. Typical content includes grand quests, mythical creatures, and richly diverse worlds populated by elves, dwarves, dragons, and gods. Thematic elements emphasize personal heroism, moral choices, and exploration of ancient ruins or magical realms. Visual cues often feature towering castles, enchanted forests, glowing magical runes, and iconic fantasy weapons like swords and staffs. Characters are vividly designed with detailed armor, cloaks, or mystical talismans, often carrying a sense of grandeur or individuality. This theme often invokes a sense of epic scale, vibrant magic, and the ever-present thrill of danger."
    if style == "Vampire: The Masquerade":
        styleStr = "The Vampire: The Masquerade theme is drenched in gothic elegance, focused on the dark and seductive lives of vampires navigating a world of political intrigue and ancient secrets. Content explores themes of immortality, forbidden desire, moral decay, and the struggle between humanity and the beast within. The setting often blends urban environments with shadowy alleys, opulent mansions, and candlelit cathedrals. Visual cues include pale, alluring characters in dark, stylish clothing, crimson accents symbolizing blood, and moonlit cityscapes. The overall aesthetic is a fusion of gothic romance and modern grit, creating a somber yet intoxicating atmosphere."
    if style == "Call of Cthulhu":
        styleStr = "The Call of Cthulhu theme delves into cosmic horror, focusing on the fragility of the human mind when confronted with incomprehensible, otherworldly forces. Content often includes cults, forbidden knowledge, eldritch creatures, and settings that exude unease, such as decaying mansions, mist-shrouded harbors, and ancient, forbidden libraries. Thematic elements revolve around madness, fear of the unknown, and the insignificance of humanity in a vast, uncaring universe. Visual cues include dark, foreboding colors, intricate carvings of monstrous beings, and eerie coastal or forested landscapes. The aesthetic leans heavily on unsettling, shadowy imagery and a pervading sense of dread."
    if style == "Shadowrun":
        styleStr = "The Shadowrun theme blends cyberpunk and urban fantasy, presenting a gritty world where advanced technology coexists with magic. Content includes cyber-enhanced characters, magical beings like orcs and elves, and sprawling megacities dominated by neon lights and corporate logos. Thematic elements explore corporate greed, resistance to oppression, and the fusion of the digital and magical realms. Visual cues feature cybernetic implants, augmented reality overlays, spellcasting integrated with technology, and dark cityscapes with glowing signs and rain-soaked streets. The aesthetic is a unique mix of high-tech futurism and mystical arcana, creating a vibrant yet shadowy world."
    if style == "No TTRPG Theme/Use Real World":
        styleStr = "The Reality or Real World theme is grounded in the familiar, focusing on everyday experiences, contemporary issues, and authentic human emotions. Content spans a wide range of topics, from personal drama and social commentary to slice-of-life depictions of mundane activities. Thematic elements emphasize relatability, the passage of time, and human connection. Visual cues include realistic settings such as bustling urban streets, suburban homes, or natural landscapes. Characters are depicted with genuine imperfections, wearing everyday attire. The aesthetic is straightforward and unembellished, often using natural light and subtle tones to create a sense of authenticity and immediacy."
    return styleStr


def generate_image(ttrpg_text, style_text, character_text, eye_text, hair_text, expression_text, body_text, clothing_text, props_text, ar, Use_Image, input_image, Use_Face):
    if input_image is None:
        pass
    else:
        image = Image.fromarray(input_image)
        my_time = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S.%f")
        save_dir = INPUT_DIR + "input_" + my_time + ".png"
        image.save(save_dir)

    with open("workflow_api_TTRPGImage.json", "r", encoding="utf8") as file_json:
        prompt = json.load(file_json)
        if ar == "1:1":
            prompt["27"]["inputs"]["width"] = 1152
            prompt["27"]["inputs"]["height"] = 1152
        if ar == "3:4":
            prompt["27"]["inputs"]["width"] = 864
            prompt["27"]["inputs"]["height"] = 1152
        if ar == "4:3":
            prompt["27"]["inputs"]["width"] = 1152
            prompt["27"]["inputs"]["height"] = 864
        prompt["74"]["inputs"]["text"] = "Overall Theme: " + getTheme(ttrpg_text) + ". Style (Maintain this style by ensuring to add descriptors that prompt this style): " + getStyle(
            str(style_text),
            prompt) + ". The subject is described as: " + character_text + eye_text + hair_text + expression_text + body_text + clothing_text + props_text + " (You can expand on the previous, but do not lose any details in the generated prompt) and you will add additional details and elaboration as needed based on the theme and style. Place the subject in a setting that fits the theme, style, and subject, and elaborate and describe the background and setting."
        prompt["25"]["inputs"]["noise_seed"] = random.randint(1, 999999999999999)
        if Use_Image == useImage_options[1]:
            prompt["94"]["inputs"]["boolean"] = not prompt["94"]["inputs"]["boolean"]
            prompt["70"]["inputs"]["image"] = save_dir
        if Use_Face == useImage_options[1]:
            prompt["188"]["inputs"]["boolean"] = not prompt["188"]["inputs"]["boolean"]
            prompt["70"]["inputs"]["image"] = save_dir
    start_queue(prompt)
    previous_image = get_latest_image(OUTPUT_DIR)
    while True:
        latest_image = get_latest_image(OUTPUT_DIR)
        if latest_image != previous_image:
            break
        time.sleep(2)
    return latest_image


def generate_video(input_image, anim_text):
    if input_image is None:
        stop_queue()
        return
    else:
        image = Image.fromarray(input_image)
        my_time = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S.%f")
        save_dir = INPUT_DIR + "input_" + my_time + ".png"
        image.save(save_dir)

    with open("workflow_api_video.json", "r", encoding="utf8") as file_json:
        prompt = json.load(file_json)
    prompt["333"]["inputs"]["text"] = anim_text
    prompt["70"]["inputs"]["image"] = save_dir
    start_queue(prompt)
    previous_video = get_latest_video(OUTPUT_DIR)
    while True:
        latest_video = get_latest_video(OUTPUT_DIR)
        if latest_video != previous_video:
            time.sleep(10)
            break
        time.sleep(2)
    return latest_video

def generate_avatarInstant(input_image0, input_image1):
    if input_image0 is None or input_image1 is None:
        stop_queue()
        return
    else:
        image0 = Image.fromarray(input_image0)
        my_time = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S.%f")
        save_dir0 = INPUT_DIR + "input_" + my_time + ".png"
        image0.save(save_dir0)
        image1 = Image.fromarray(input_image1)
        my_time = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S.%f")
        save_dir1 = INPUT_DIR + "input_" + my_time + ".png"
        image1.save(save_dir1)

    with open("workflow_api_instantAvatar.json", "r", encoding="utf8") as file_json:
        prompt = json.load(file_json)
    prompt["70"]["inputs"]["image"] = save_dir0
    prompt["635"]["inputs"]["image"] = save_dir1
    start_queue(prompt)
    previous_image = get_latest_image(OUTPUT_DIR)
    while True:
        latest_image = get_latest_image(OUTPUT_DIR)
        if latest_image != previous_image:
            break
        time.sleep(2)
    return latest_image


ar_options = ["1:1", "3:4", "4:3"]
ar_radio = gr.Radio(ar_options, value="1:1", label="Choose an aspect ration (Default 1:1)")
useImage_options = ["No", "Yes"]
useImage_radio = gr.Radio(useImage_options, value="No",
                          info="Best to include an image that has a Person from at least the waist up.",
                          label="Do you want to use an uploaded image to guide the generation? This will guide aspects of the images pose and shot.")
useFace_options = ["No", "Yes"]
useFace_radio = gr.Radio(useFace_options, value="No", label="Do you want to swap your face in the image?",
                         info="Choose no if you chose not to upload an image or there is no face in the image. If you chose not to control guide the image you can still use this to swap your face, assuming a face appears in the generated image. Results will be better if guided and no more than 3/4 turned.")

ttrpg_input = gr.Textbox(label="Type in a TTRPG or Media Franchise")
ttrpg_dropdown = gr.Dropdown(
    choices=["Dungeons and Dragons/Pathfinder", "Vampire: The Masquerade", "Call of Cthullu", "Shadowrun", "Cyberpunk",
             "No TTRPG Theme/Use Real World"], label="Choose a TTRPG")
style_input = gr.Textbox(label="Type in a description of the desired art style")
style_dropdown = gr.Dropdown(
    choices=["Hyper-Realistic Oil Painting", "Anime/Manga", "Film Quality 3D Render", "Live-Action Film Still",
             "Professional Photograph", "Amateur Photograph", "Realistic Cartoon"], label="Choose an Art Style")
characterdesc_input = gr.Textbox(label="Describe your characters gender, class, and setting",
                                 info="Example: A male paladin stands in a cathedral to the goddess tiamat.")
characterDetail_Eye = gr.Textbox(label="Describe your characters eye's and eye color",
                                 info="Example: He has red eyes and a furrowed brow that has a stern look.")
characterDetail_Hair = gr.Textbox(label="Describe your characters hair color and style",
                                 info="Example: He has short lilac hair.")
characterDetail_Expression = gr.Textbox(label="Describe your characters facial expression",
                                 info="Example: His face is stoic.")
characterDetail_BodyShape = gr.Textbox(label="Describe your characters Body Shape (e.g., Height and Weight descriptors, Bust Size, Figure(Hourglass, Pear, Petite etc.), Musculature)",
                                 info="Example: He is above average in height and has broad shoulders. He has well-defined muscles.")
characterDetail_Clothing = gr.Textbox(label="Describe your characters Clothing, and that clothing's positioning and condition.",
                                 info="Example: He wears obsidian black platemail, with raven motifs in silver. He wears a purple cape.")
characterDetail_PoseProps = gr.Textbox(label="Describe your characters pose and additional props.",
                                 info="Example: He is wielding a massive greatsword in his left hand, and he stands in a dominating stance.")



character_interface = gr.Interface(
    fn=generate_image,
    title="TTRPG Characterinator",
    description='Use this App to generate an RPG Character portrait, and even add your face if you want.',

    inputs=[ttrpg_dropdown, style_dropdown, characterdesc_input, characterDetail_Eye, characterDetail_Hair, characterDetail_Expression, characterDetail_BodyShape, characterDetail_Clothing, characterDetail_PoseProps, ar_radio, useImage_radio, "image", useFace_radio],
    outputs=["image"],
)

animText_input = gr.Textbox(
    label="Add additional movement or animation instructions here for your Avatar to help guide the final video")

animate_interface = gr.Interface(
    fn=generate_video,
    title="Avatar Animator",
    description="Use this App to generate an animate your character portrait. \nUpload an image that is at least 768px wide. \nThe output will be 768x512, but will attempt to crop to a face. \nIf there is no face or one is undetected it will crop from center scaled by the width.",

    inputs=["image", animText_input],
    outputs=["video"],
)

faceAvatar_image = gr.Image(label="Upload and Image of your face")
characterAvatar_image = gr.Image(label="Upload your character inspiration")

instantAvatar_interface = gr.Interface(
    fn=generate_avatarInstant,
    title="Instant Avatar",
    description="Use this App to generate an Avatar with just two images. \nUpload an image of your face and artwork of your choice. \nThe output will be a 1024x1024 image combining you with the content of the other.",

    inputs=[faceAvatar_image, characterAvatar_image],
    outputs=["image"],
)

demo = gr.TabbedInterface([character_interface, animate_interface, instantAvatar_interface], ["TTRPG Characterinator", "Avatar Animator", "Instant Avatar"])
demo.queue(default_concurrency_limit=1)
demo.launch(allowed_paths=[OUTPUT_DIR], share=True)
