from flask import Flask, url_for
from flask import request
import requests
from flask_cors import CORS
import json
from flask import jsonify
import random
import praw
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
CORS(app)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/', methods=['GET'])
def index():
    return site_map()


@app.route('/site-map', methods=['GET'])
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if not url == '/site-map':
                links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    if len(links) > 0:
        return jsonify({"success":True,"routes":links})
    else:
        return jsonify({"success":False,"routes":links})


@app.route('/generate_image', methods=['POST'])
def generate_image():
    url = request.args['url']
    name = request.args['name']
    top = request.args['top']
    bottom = request.args['bottom']

    # get the image from url

    # open the image and get some properties
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    img = Image.open(r.raw).convert('RGB')
    size = width, height = img.size

    #need to figure out where to put text and how big based on the size of the image
    # at 60px figure a letter is about 30x60px
    # so then using the number of letters and image width, figure out if
    # a newline is needed and where to start
    text_size = height / 12

    draw = ImageDraw.Draw(img,'RGB')
    font = ImageFont.truetype("impact.ttf", text_size)
    
    top_width = font.getsize(top)[0]
    top_start_x = (width / 2) - (top_width / 2)
    bottom_width = font.getsize(bottom)[0]
    bottom_start_x = (width / 2) - (bottom_width / 2)

    # this is broken, instead of adding \n and drawing once
    # split up into multiple strings and draw multiple times
    # with \n version, the text width given by pillow is incorrect
    # if top_width > width:
    #     print(top_width)
    #     top_chars = len(top)
    #     copy = top
    #     copy.split(' ')
    #     total = 0
    #     for word in copy:
    #         total += len(word)
    #         if total > (top_chars / 2):
    #             break
    #         total += 1
    #     print(total)
    #     print(top[:total-2])
    #     new_text = top[:total-2] + '\n' + top[total-2:]
    #     print(new_text)
    #     top = new_text
    #     top_width = font.getsize(new_text)[0]
    #     print(font.getsize(new_text))
    #     print('new top width ', top_width)
    #     top_start_x = (width / 2) - (top_width / 2)
    #     bottom_width = font.getsize(bottom)[0]
    #     bottom_start_x = (width / 2) - (bottom_width / 2)

    draw_text(draw, top_start_x, 10, top, (255, 255, 255), (0, 0, 0), font)
    draw_text(draw, bottom_start_x, height-text_size-10, bottom, (255, 255, 255), (0, 0, 0), font)

    img.save('../html/img/' + name + '.jpg')
    
    return jsonify({"success":True,"url":'img/' + name + '.jpg',"top":top,"bottom":bottom})

def draw_text(draw, x, y, text, fillcolor, outlinecolor, font):
    draw.text((x-2, y), text, fill=outlinecolor, font=font)
    draw.text((x+2, y), text, fill=outlinecolor, font=font)
    draw.text((x, y-2), text, fill=outlinecolor, font=font)
    draw.text((x, y+2), text, fill=outlinecolor, font=font)
    draw.text((x, y), text, fillcolor,font=font)

@app.route('/get_image', methods=['GET'])
def get_image():
    # id = request.args['id']

    # return jsonify({"success":True,"id":id})

    return send_file(filename, mimetype='image/gif')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
