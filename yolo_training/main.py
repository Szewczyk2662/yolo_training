import json
import os
import shutil


def convert_json_to_yolo(json_file, json_dir, img_dir, output_label_dir, output_image_dir):
    # Wczytaj plik JSON
    json_path = os.path.join(json_dir, json_file)
    print(f"Wczytywanie pliku JSON: {json_path}")  # Debugowanie
    with open(json_path) as f:
        data = json.load(f)

    # Pobierz rozmiar obrazu z pliku JSON
    img_width = data['size']['width']
    img_height = data['size']['height']

    # Lista do przechowywania danych YOLO
    yolo_data = []

    # Przetwarzanie obiektów w JSON
    for obj in data['objects']:
        # Mapowanie classTitle na class_id (upewnij się, że masz pełną listę klas)
        class_title = obj['classTitle']
        class_id = class_title_to_id.get(class_title)
        if class_id is None:
            print(f"Nieznana klasa: {class_title}")
            continue  # Pomijaj nieznane klasy

        x_min, y_min = obj['points']['exterior'][0]
        x_max, y_max = obj['points']['exterior'][1]

        # Obliczenia do formatu YOLO
        x_center = ((x_min + x_max) / 2) / img_width
        y_center = ((y_min + y_max) / 2) / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height

        yolo_data.append(f"{class_id} {x_center} {y_center} {width} {height}")

    # Zapisz etykiety w formacie YOLO
    label_output_file = os.path.join(output_label_dir, os.path.splitext(json_file)[0] + ".txt").replace('.png', '')
    with open(label_output_file, 'w') as out_f:
        out_f.write("\n".join(yolo_data))

    # Skopiuj odpowiadający obraz do katalogu docelowego
    image_file_base = os.path.splitext(json_file)[0]  # Usunięcie tylko rozszerzenia .json, pozostawiając .png
    image_file = image_file_base  # Bez dodawania rozszerzeń, ponieważ nazwa już je ma

    src_image_path = os.path.join(img_dir, image_file)
    print(f"Sprawdzanie ścieżki: {src_image_path}")  # Debugowanie - wyświetla pełną ścieżkę do obrazu
    if os.path.exists(src_image_path):
        print(f"Znaleziono obraz: {src_image_path}")
        dst_image_path = os.path.join(output_image_dir, image_file)
        shutil.copyfile(src_image_path, dst_image_path)
    else:
        print(f"Brak obrazu dla pliku JSON: {json_file}")


# Słownik mapujący nazwy klas na ID (upewnij się, że zawiera wszystkie klasy)
class_title_to_id = {
    'orange_cone': 0,
    'large_orange_cone': 1,
    'blue_cone': 2,
    'yellow_cone': 3
    # Dodaj inne klasy, jeśli istnieją
}


def process_all_jsons(json_dir, img_dir, output_label_dir, output_image_dir):
    # Upewnij się, że katalogi wyjściowe istnieją
    os.makedirs(output_label_dir, exist_ok=True)
    os.makedirs(output_image_dir, exist_ok=True)

    # Przetwarzaj wszystkie pliki JSON
    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            convert_json_to_yolo(json_file, json_dir, img_dir, output_label_dir, output_image_dir)


# Ścieżki do katalogów (dostosuj do swojej struktury)
json_dir = r'/home/szewczyk/Desktop/dataset/ann'  # Katalog z plikami JSON
img_dir = r'/home/szewczyk/Desktop/dataset/img'  # Katalog z obrazami
output_label_dir = r'/home/szewczyk/Desktop/Yolo/labels'  # Katalog docelowy etykiet YOLO
output_image_dir = r'/home/szewczyk/Desktop/Yolo/out_img'  # Katalog docelowy obrazów

# Przetwarzaj wszystkie pliki JSON
process_all_jsons(json_dir, img_dir, output_label_dir, output_image_dir)
