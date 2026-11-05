from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)
shortened_urls = {} # the dictionary stores the mapping of short urls to their long urls.

# this function generates the random short url of 6 characters out of the long url
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

# this index route handles both get and post requests. It routes the short url to the long one.
@app.route('/', methods=['GET', 'POST'])

#
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = generate_short_url()

        # If the short_url has been taken, regenerate another to avoid duplicate urls
        while short_url in shortened_urls:
            short_url = generate_short_url()

        # return the full url, the shortened url and the original root url
        shortened_urls[short_url] = original_url
        return f"Shortened URL: {request.url_root}{short_url}"

    # return if it is GET request, it would render the index.html file which contains the form to input the long url.
    return render_template('index.html')


# the redirection 
@app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = shortened_urls.get(short_url)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)

