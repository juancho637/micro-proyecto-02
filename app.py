import io
from PIL import Image
import flask
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.models as models
import requests

app = flask.Flask(__name__)

# Cargar el modelo preentrenado en ImageNet (ResNet18)
model = models.resnet18(pretrained=True)
model.eval()

# Descargar el mapeo de índices a etiquetas de ImageNet
url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
response = requests.get(url)
imagenet_class_index = response.json()

# Definir el mapeo de palabras clave para cada clase de CIFAR-10
cifar_mapping = {
    "airplane": ["airplane", "airliner", "warplane"],
    "automobile": ["car", "automobile", "convertible", "limousine", "sedan"],
    "bird": ["bird", "hen", "robin", "sparrow"],
    "cat": ["cat", "tiger", "lion", "kitten"],
    "deer": ["deer"],
    "dog": ["dog", "labrador", "poodle", "retriever", "basenji", "terrier"],
    "frog": ["frog", "toad"],
    "horse": ["horse"],
    "ship": ["ship", "boat", "vessel"],
    "truck": ["truck", "lorry"]
}

# Lista de clases de CIFAR-10 para referencia
cifar_classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                 'dog', 'frog', 'horse', 'ship', 'truck']

# Preprocesamiento según lo que espera ResNet18 en ImageNet
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
         mean=[0.485, 0.456, 0.406],
         std=[0.229, 0.224, 0.225]
    )
])

@app.route("/predict", methods=["POST"])
def predict():
    if "img" not in flask.request.files:
        return flask.jsonify({"error": "No image provided"}), 400

    # Leer y preprocesar la imagen
    image_file = flask.request.files["img"]
    img = Image.open(io.BytesIO(image_file.read())).convert("RGB")
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0)

    # Realizar la predicción
    with torch.no_grad():
        output = model(input_batch)
    probabilities = F.softmax(output[0], dim=0)
    top_prob, top_idx = torch.max(probabilities, dim=0)

    # Obtener el label de ImageNet
    imagenet_label = imagenet_class_index[str(top_idx.item())][1]
    
    pred_label_lower = imagenet_label.lower()
    mapped_label = None
    for cifar_class, keywords in cifar_mapping.items():
        for kw in keywords:
            if kw in pred_label_lower:
                mapped_label = cifar_class
                break
        if mapped_label is not None:
            break

    # Si no se encuentra coincidencia, asignar la etiqueta original de ImageNet
    if mapped_label is None:
        mapped_label = imagenet_label

    result = {
        "prediction": mapped_label,
        "probability": top_prob.item()
    }
    return flask.jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
