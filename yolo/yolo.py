from ultralytics import YOLO


class YOLOModel:
    def __init__(self, path: str):
        self.model = YOLO(path)

    def predict_best_class(self, image):
        results = self.model.predict(image)
        probs = results[0].probs
        best_class_idx = probs.top1  # índice da classe mais provável
        best_class_name = self.model.names[best_class_idx]
        return best_class_name
