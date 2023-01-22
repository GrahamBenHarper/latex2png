# latex2png
A simple Flask-based application for rendering LaTeX equations as `.png` images.

### Requirements
This requires the python package `flask` to run the application. It additionally requires `texlive-latex-base`, and `imagemagick`. Specifically, the commands `pdflatex` and `convert` from the latter two packages should be available in your `$PATH`.

For example, on many Linux-based systems, one can simply install the necessary packages with
```
sudo apt install python3-pip texlive-latex-base imagemagick
pip3 install flask
```

This has been tested on Ubuntu 20.04 and 22.04.

### Running the application

The application is run by running `app.py`. Then, the content should be visible on `127.0.0.1:5000` in any web browser. Simply enter an equation into the text field and click the submit button.

![latex2png](https://user-images.githubusercontent.com/12531152/213901306-70c66878-a678-4040-8539-1dc81c1cc30d.gif)

### Troubleshooting

When running the app for the first time, you may see an image that says the pdf to png conversion failed. If you check the terminal, one of the most common issues you will see is the following:
```
convert-im6.q16: attempt to perform an operation not allowed by the security policy `PDF' @ error/constitute.c/IsCoderAuthorized/421.
convert-im6.q16: no images defined `equation.png' @ error/convert.c/ConvertImageCommand/3229.
```

To fix this, simply modify ImageMagick's `policy.xml` file (located in `/etc/ImageMagick-6/policy.xml` on Linux-based systems)
```
  <policy domain="coder" rights="none" pattern="PDF" />
```
and add comment braces around the above line so it reads as
```
  <!-- <policy domain="coder" rights="none" pattern="PDF" /> -->
```

Once those changes are saved, subsequent clicks on the submit button should behave as intended.
