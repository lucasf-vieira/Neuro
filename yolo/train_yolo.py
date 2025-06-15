from ultralytics import YOLO
from pathlib import Path
import torch

# Configurações
model_arch = 'yolov8s-cls.pt'     # Arquitetura base (nano, small, medium...)
dataset_path = 'dataset'          # Dataset com pasta train/ e val/
imgsz = 224                       # Tamanho da imagem de entrada
epochs = 20
batch = 16

# Treinamento
model = YOLO(model_arch)
model.train(
    data=dataset_path,
    epochs=epochs,
    imgsz=imgsz,
    batch=batch
)

# Caminho do modelo treinado
trained_model_path = model.ckpt_path if hasattr(model, 'ckpt_path') else model.trainer.best

# Carregar o modelo treinado
model = YOLO(trained_model_path)

# Previsão em uma imagem individual
test_image = Path("dataset/train/red")
results = model.predict(test_image)

# Exibir resultados
for r in results:
    probs = r.probs
    top_class = probs.top1
    class_name = model.names[top_class]
    confidence = probs[top_class].item()
    print(f'Classe: {class_name}, Confiança: {confidence:.2f}')

model.save("../model.pt")
