import os

root_path = os.path.dirname(os.path.abspath(__file__))

IMAGES = (
    (os.path.join(root_path, 'static/cat.png'), 'PNG', 960, 603),
    (os.path.join(root_path, 'static/cat-png'), 'PNG', 960, 603),
    (os.path.join(root_path, 'static/spongebob.gif'), 'GIF', 500, 334),
    (os.path.join(root_path, 'static/spongebob-gif'), 'GIF', 500, 334),
    (os.path.join(root_path, 'static/happy_dog.gif'), 'GIF', 370, 370),
    (os.path.join(root_path, 'static/happy_dog-gif'), 'GIF', 370, 370),
)

UNSUPPORTED_IMAGES = (
    os.path.join(root_path, 'static/homer.svg'),
)
