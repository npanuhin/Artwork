<h1 class="gp_hidden"><p align="center">Vector images</p></h1>

<div class="badges gp_hidden" align="center">
	<a href="./SVG" title="Average SVG size: {average_svg_size}"><img alt="Average SVG size: {average_svg_size}" src="https://img.shields.io/static/v1?cacheSeconds=10800&style=flat&label=Average%20SVG%20size&message={average_svg_size_url}&color=0aa"></a>
	<a href="./SVG" title="Average compressed SVG size: {average_compressed_svg_size}"><img alt="Compressed: {average_compressed_svg_size}" src="https://img.shields.io/static/v1?cacheSeconds=10800&style=flat&label=Compressed&message={average_compressed_svg_size_url}&color=bb0"></a>
	<a href="./src/SVG_sample.md" target="_blank" title="SVG version: 1.1"><img alt="SVG version: 1.1" src="https://img.shields.io/static/v1??cacheSeconds=86400&style=flat&label=SVG&message=v1.1&color=orange"></a>
	<a href="http://n-panuhin.info/license.html" target="_blank" title="license: MIT"><img alt="license: MIT" src="https://img.shields.io/static/v1?cacheSeconds=604800&style=flat&label=license&message=MIT&color=informational"></a>
</div>

## About

This is a repository of vector images that I made while studying vector graphics (templates were taken from the Internet, but all vector pictures were drawn by me).

**[Start exploring!](./SVG "See SVG images")**

**If you think that you have found a mistake or have sufficiently improved (including minification) something in this repository, you are very welcome to contact me <a href="http://n-panuhin.info" title="Nikita Panuhin" target="_blank">here</a> or directly by [email](mailto:n.panuhin@mail.ru "Mailto: Nikita Panuhin").**

You can use any of these images in your projects, works etc within the confines of the license.

## How to use

Each SVG image has a colored or/and black-and-white version. You can use (download):

-   Beautified colored version
-   Compressed colored version
-   Beautified black-and-white version
-   Compressed black-and-white version
-   *Adobe Illustrator* source files

Links are located at the bottom of each page.

## Technical information

-   Adobe Illustrator files are built with *Illustrator CC* and are compatible with *Illustrator 17* and later versions.
-   SVG files are exported from Adobe Illustrator and then partly minified and beautified to fit some standards, as I see it. <a href="https://github.com/Nikita-Panyuhin/vector/blob/master/src/SVG_sample.md" title="See SVG file sample" target="_blank">See sample</a>
-   PNG files are rendered using the *<a href="https://github.com/neocotic/convert-svg/tree/master/packages/convert-svg-to-png" title="Node.js: convert-svg-to-png by neocotic" target="_blank">convert-svg-to-png</a>* Node.js package by <a href="https://github.com/neocotic" title="Github user: neocotic" target="_blank">neocotic</a>. Render sizes are specified for each image in "SVG/{{image\_name}}/src/conf.json".
-   The size of any SVG image is calculated without considering the size of the XML header (-40 bytes). SVG version is removed for compressed files (-14 bytes).

--------------------------------------

Copyright &copy; 2020 Nikita Paniukhin

License: [MIT](http://n-panuhin.info/license.html "Visit n-panuhin.info/license")