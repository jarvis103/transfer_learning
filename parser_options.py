import argparse

training_parser = argparse.ArgumentParser()
training_parser.add_argument(
    '--image_dir',
    type=str,
    default=r'~/flower_photos',
    help='Path to folders of labeled images.'
)
training_parser.add_argument(
    '--output_graph',
    type=str,
    default=r'/tmp/output_graph.pb',
    help='Where to save the trained graph.'
)
training_parser.add_argument(
    '--intermediate_output_graphs_dir',
    type=str,
    default=r'/tmp/intermediate_graph',
    help='Where to save the intermediate graphs.'
)
training_parser.add_argument(
    '--intermediate_store_frequency',
    type=int,
    default=100,
    help='How many steps to store intermediate graph. If "0" then will not store.'
)
training_parser.add_argument(
    '--output_labels',
    type=str,
    default=r'/tmp/output_labels.txt',
    help=r'Where to save the trained graph\'s labels.'
)
training_parser.add_argument(
    '--summaries_dir',
    type=str,
    default=r'/tmp/retrain_logs',
    help='Where to save summary logs for TensorBoard.'
)
training_parser.add_argument(
    '--how_many_training_steps',
    type=int,
    default=4000,
    help='How many training steps to run before ending.'
)
training_parser.add_argument(
    '--learning_rate',
    type=float,
    default=1e-4,
    help='How large a learning rate to use when training.'
)
training_parser.add_argument(
    '--beta1',
    type=float,
    default=0.9,
    help='beta1 param of ADAM optimizer'
)
training_parser.add_argument(
    '--beta2',
    type=float,
    default=0.999,
    help='beta2 param of ADAM optimizer'
)
training_parser.add_argument(
    '--epsilon',
    type=float,
    default=1e-8,
    help='Optimizer hyperparam'
)
training_parser.add_argument(
    '--decay',
    type=float,
    default=0.9,
    help='RMSProp decay param.'
)
training_parser.add_argument(
    '--momentum',
    type=float,
    default=0.0,
    help='RMSProp momentum param.'
)
training_parser.add_argument(
    '--testing_percentage',
    type=int,
    default=10,
    help='What percentage of images to use as a test set.'
)
training_parser.add_argument(
    '--validation_percentage',
    type=int,
    default=10,
    help='What percentage of images to use as a validation set.'
)
training_parser.add_argument(
    '--eval_step_interval',
    type=int,
    default=10,
    help='How often to evaluate the training results.'
)
training_parser.add_argument(
    '--train_batch_size',
    type=int,
    default=32,  # 'MUST' be power of 2
    help='How many images to train on at a time.'
)
training_parser.add_argument(
    '--test_batch_size',
    type=int,
    default=-1,
    help="""
      How many images to test on. This test set is only used once, to evaluate
      the final accuracy of the model after training completes.
      A value of -1 causes the entire test set to be used, which leads to more
      stable results across runs."""
)
training_parser.add_argument(
    '--validation_batch_size',
    type=int,
    default=-1,
    help=r"""
      How many images to use in an evaluation batch. This validation set is
      used much more often than the test set, and is an early indicator of how
      accurate the model is during training.
      A value of -1 causes the entire validation set to be used, which leads to
      more stable results across training iterations, but may be slower on large
      training sets."""
)
training_parser.add_argument(
    '--bottleneck_dir',
    type=str,
    default=r'/tmp/bottleneck',
    help='Path to cache bottleneck layer values as files.'
)
training_parser.add_argument(
    '--final_tensor_name',
    type=str,
    default='final_result',
    help='Name of the output classification layer in the retrained graph.'
)
training_parser.add_argument(
    '--optimizer',
    type=str,
    default='adam',
    help="The name of the output classification layer in the retrained graph."
)
training_parser.add_argument(
    '--flip_left_right',
    default=False,
    help=r'Randomly flip half of the images.',
    action='store_true'
)
training_parser.add_argument(
    '--random_crop',
    type=int,
    default=0,
    help='A percentage determining how much of a margin to randomly crop off the training images.'
)
training_parser.add_argument(
    '--random_scale',
    type=int,
    default=0,
    help=r'A percentage determining how much to randomly scale up the size of the training images by.'
)
training_parser.add_argument(
    '--random_brightness',
    type=int,
    default=0,
    help="""\
      A percentage determining how much to randomly multiply the training image
      input pixels up or down by.\
      """
)

# "https://tfhub.dev/google/imagenet/inception_resnet_v2/feature_vector/1"
# "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1"
# "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/1"
training_parser.add_argument(
    '--tfhub_module',
    type=str,
    default='https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1',
    help='Which TensorFlow Hub module to use.')

training_parser.add_argument(
    '--saved_model_dir',
    type=str,
    default='',
    help='Where to save the exported graph.')

training_parser.add_argument(
    '--checkpoint_path',
    type=str,
    default=r'/tmp/checkpoints',
    help='Checkpoints location.')

training_parser.add_argument(
    '--min_images_per_label',
    type=int,
    default=20,
    help='Label folders with less than this number will NOT be used.')

training_parser.add_argument(
    '--max_images_per_label',
    type=int,
    default=2 ** 16,
    help='Label folders with more than this number will NOT be used.')

FLAGS, unparsed = training_parser.parse_known_args()

FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars', 'FakeQuantWithMinMaxVarsPerChannel')

test_parser = argparse.ArgumentParser()
test_parser.add_argument("--image", default="tensorflow/examples/label_image/data/grace_hopper.jpg", help="image to be processed")
test_parser.add_argument("--graph", default="tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb", help="graph/model to be executed")
test_parser.add_argument("--labels", default="tensorflow/examples/label_image/data/imagenet_slim_labels.txt", help="name of file containing labels")
test_parser.add_argument("--input_height", default=299, type=int, help="input height")
test_parser.add_argument("--input_width", default=299, type=int, help="input width")
test_parser.add_argument("--input_mean", default=0, type=int, help="input mean")
test_parser.add_argument("--input_std", default=255, type=int, help="input std")
test_parser.add_argument("--input_layer", default="input", help="name of input layer")
test_parser.add_argument("--output_layer", default="InceptionV3/Predictions/Reshape_1", help="name of output layer")
testFLAGS = test_parser.parse_args()
