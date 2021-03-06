import argparse
from sys import argv
from Almacen import *
from Algoritmos import *

if __name__ == "__main__":

    wh = Warehouse()
    d = Detector()

    parser = argparse.ArgumentParser(
        description='Entrena sober train y ejecuta el clasificador sobre imgs de test')
    parser.add_argument(
        '--train_path', type=str, default="./train", help='Path al directorio de imgs de train')
    parser.add_argument(
        '--test_path', type=str, default="./test", help='Path al directorio de imgs de test')
    parser.add_argument(
        '--classifier', type=str, default="HOG_LDA_BAYES", help='String con el nombre del clasificador')

    args = parser.parse_args()
    argv = args.train_path, args.test_path, args.classifier

    nombres_clasificadores = ["HOG_LDA_BAYES", "GRAY_LDA_BAYES", "RGB_LDA_BAYES",
                              "CANY_LDA_BAYES", "HOG_PCA_KNN", "GRAY_PCA_KNN", "RGB_PCA_KNN", "CANY_PCA_KNN"]

    # check if the number of arguments is correct print the help if not
    if len(argv) != 3:
        parser.print_help()
        exit(1)

    if args.classifier not in nombres_clasificadores:
        print("Error: el clasificador no es valido")
        parser.print_help()
        exit(1)
    if not os.path.isdir(args.train_path):
        print("Error: el directorio de train no existe")
        parser.print_help()
        exit(1)
    if not os.path.isdir(args.test_path):
        print("Error: el directorio de test no existe")
        parser.print_help()
        exit(1)

    classifier_type = args.classifier.upper().split('_')
    # Cargar los datos de entrenamiento
    wh.load_train_images(args.train_path)
    # Tratamos los datos en funcion del clasificador
    wh.data_treatment(classifier_type)
    # Cargar los datos de test
    wh.load_test_images(args.test_path)
    # Clasificar los datos de test y almacenamiento
    wh.save_images(d.multiclass_classifier(
        wh.test_images, wh.clasificadores_binarios, wh.knn, wh.pca, classifier_type))
    # Evaluar el clasificador
    #d.evaluate_classifier(wh.validation_set, wh.clasificadores_binarios, wh.knn, wh.pca, classifier_type)
