# latex2png
A simple Flask-based application for rendering LaTeX equations as `.png` images.

### Requirements
This requires the python package Flask to run the application. It additionally requires texlive-latex-base, and imagemagick. Specifically, the commands `pdflatex` and `convert` from the latter two packages should be available in your `$PATH`. This has been tested on Ubuntu 22.04.

### Running the application

The application is run by running `app.py`. Then, the content should be visible on `127.0.0.1:5000` in any web browser. Simply enter an equation into the text field and click the submit button.

![tutorial](https://user-images.githubusercontent.com/12531152/194993345-a677d9df-bcd2-4cf2-8e86-444b7814aa74.gif)

### Troubleshooting

When converting pdf files to images, you may see the following error:
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
