import datetime
import configparser
from base64 import b64decode
from flask import Flask, render_template, request
import openai
from openai.error import InvalidRequestError


def generate_image(prompt, num_image=1, size='512x512', output_format='url'):
    """
    params:
        prompt (str):
        num_image (int):
        size (str):
        output_format (str):
    """
    try:
        images = []
        response = openai.Image.create(
            prompt=prompt,
            n=num_image,
            size=size,
            response_format=output_format
        )
        if output_format == 'url':
            for image in response['data']:
                images.append(image.url)
        elif output_format == 'b64_json':
            for image in response['data']:
                images.append(image.b64_json)
        return {'created': datetime.datetime.fromtimestamp(response['created']), 'images': images}
    except InvalidRequestError as e:
        print(e)


app = Flask(__name__)

config = configparser.ConfigParser()
config.read('credential.ini')
API_KEY = config['openai']['APIKEY']

openai.api_key = API_KEY

SIZES = ('256x256', '512x512', '256x256')


@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = generate_image(prompt, num_image=1, size=SIZES[0])
        if response is not None:
            image_url = response['images'][0]
    return render_template('index.html', image_url=image_url)


if __name__ == '__main__':
    app.run()
