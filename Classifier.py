from taipy.gui import Gui
from tensorflow.keras import models
from PIL import Image
import numpy as np

class_names = {
    0: 'airplane',
    1: 'automobile',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck',
}

model = models.load_model("baseline.keras",compile=False)

def predict_image (model,path_to_image):
    img = Image.open(path_to_image)
    img = img.convert("RGB")
    img = img.resize((32,32))
    data = np.asarray(img)
    data = data/255
    probs = model.predict(np.array([data])[:1])
    
    top_prob = probs.max()
    top_pred = class_names[np.argmax(probs)]
    return top_prob, top_pred

  

content = ""
image_path = "placeholder_image.png"
prob = 0
pred = ""
index = """
<|text-center|
<|{"logo2.png"}|image|width=400px|>

<|{content}|file_selector|extensions = .png,.jpg,.jpeg,.gif,.bmp|on_change=on_change|>
select an image form your file system

<|{pred}|>

<|{image_path}|image|>

<|{prob}|indicator|value = {prob}| min = 0| max =100|width = 400px|>


>
"""

def on_change(state,var_name,var_val):
    if var_name == "content":
        state.image_path = var_val
        top_prob, top_pred = predict_image(model,var_val)
        state.prob = round(top_prob*100)
        state.pred = "This is a "+top_pred
        state.image_path = var_val
        

app = Gui(page = index)
if __name__ == "__main__":
    app.run(use_reloader = True, debug = False , port=5001)