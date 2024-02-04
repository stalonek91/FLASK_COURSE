from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed, TEXT


app = Flask(__name__)

# photos = UploadSet('photos', IMAGES)
docs_and_pics = UploadSet('docs', TEXT + IMAGES)


app.config['UPLOADS_DEFAULT_DEST'] = 'other'
# app.config['UPLOADED_PHOTOS_ALLOW'] = ['zip']
# app.config['UPLOADED_PHOTOS_DENY'] = ['jpg']

configure_uploads(app, (docs_and_pics))


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'thefile' in request.files:
        try:
            doc_filename = docs_and_pics.save(request.files['thefile'])
            return f'File path: <h1>{docs_and_pics.url(doc_filename)}</h1>'
        except UploadNotAllowed:
            return f' FILE NOT ALLOWED KWIMKS'

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)