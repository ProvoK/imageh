import os

root_path = os.path.dirname(os.path.abspath(__file__))
join = os.path.join

IMAGES = (
    (join(root_path, 'static/cat.png'), 'PNG', 960, 603),
    (join(root_path, 'static/cat-png'), 'PNG', 960, 603),
    (join(root_path, 'static/spongebob.gif'), 'GIF', 500, 334),
    (join(root_path, 'static/spongebob-gif'), 'GIF', 500, 334),
    (join(root_path, 'static/happy_dog.gif'), 'GIF', 370, 370),
    (join(root_path, 'static/happy_dog-gif'), 'GIF', 370, 370),
)

UNSUPPORTED_IMAGES = (
    join(root_path, 'static/homer.svg'),
)
