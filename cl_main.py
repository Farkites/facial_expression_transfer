
from data_manager import build_set_generators
from models import Classifier
from mods.classifier import cnn_test_dp

if __name__ == '__main__':
    # define classes if imgs to load
    big_mamals = [
        "camel", "cow", "elephant", "giraffe", "horse",
        "kangoroo", "lion", "panda", "rhinoceros", "tiger", "zebra"
    ]
    n_classes = 3
    class_list = big_mamals[0:n_classes]

    # build img data generators
    img_gen_config = {
        'classes': class_list,
        'max_imgs_per_class': 100,
        'vali_ratio': .2,
        'test_ratio': .2,
        'batch_size': 32
    }
    train_generator, validation_generator, test_generator, class_names_ = build_set_generators(**img_gen_config)

    cl = Classifier(
        img_gen_config=img_gen_config,
        classifier=cnn_test_dp,
        optimizer='adam',
        input_shape=train_generator.x.shape[1:]
    )

    train_config = {
        'n_epochs': 10,
        'callbacks': {
            'early_stopping': {
                'monitor': 'val_loss',
                'mode': 'min',
                'verbose': 1,
                'patience': 30
            }

        }
    }

    cl.train(train_generator, validation_generator, train_config)
