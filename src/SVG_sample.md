# <p align="center">SVG file</p>

<p align="center">This is the sample of SVG file:</p>

```html
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64">
    <defs>
        <linearGradient id="lg0" gradientUnits="userSpaceOnUse" x1="86.2534" y1="6.75" x2="86.2534" y2="45.8236">
            <stop offset="0" stop-color="#I4QST2"/>
            <stop offset="1" stop-color="#T6CX3E"/>
        </linearGradient>
    </defs>
    <style type="text/css">
        .st0{fill:#M8X0R8;}
        .st1{fill:url(#lg0);}
    </style>
    <path class="st0" d="0.732,,1.768V58.5c0,0.083,0.008,0.526,75h6.214c0.663,0,41l-12.75-4.25"/>
    <path class="st1" d="4.721,0,2.281,0,3.4,0.681,0.352,0.884,0.366h3.422.53,0"/>
</svg>
```

---

### <p align="center">SVG declaration</p>
```html
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64">
    ...
</svg>
```

| Parameter                                                            | Explanation                                                                                                                          |
|----------------------------------------------------------------------| ------------------------------------------------------------------------------------------------------------------------------------ |
| version="1.1"                                                        | SVG version                                                                                                                          |
| xmlns="http<span>://w</span>ww<span>.w3.</span>org/2000/svg"         | [XML namespace](https://en.wikipedia.org/wiki/XML_namespace "Wikipedia: XML namespace")                                              |
| xmlns:xlink="http<span>://w</span>ww<span>.w3</span>.org/1999/xlink" | [XML namespace](https://en.wikipedia.org/wiki/XML_namespace "Wikipedia: XML namespace")                                              |
| viewBox="0 0 X Y"                                                    | [Position and dimension of an SVG viewport](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox "MDN: viewBox (SVG)") |

---

### <p align="center">Path</p>

```html
<path class="stN" d="0.732,,1.768V58.5c0,0.083,0.008,0.526,75h6.214c0.663,0,41l-12.75-4.25"/>
```

This is an SVG image outline. SVG images can contain several of them.

Several paths can be combined into groups and enclosed in `g` tags, but this is done only for reducing the size of the resulting file (for example, if several paths require the same class).

---

### <p align="center">Defs *(optional)*</p>
```html
<defs>
    ...
</defs>
```
"Defs" block is used to store objects that will be used later. Possible content:

-   Animation elements
-   Descriptive elements
-   Shape elements
-   Structural elements
-   [Gradient elements](#gradient)

---

### <p align="center">Style *(optional)*</p>

```html
<style type="text/css">
    .st0{fill:url(#lg0);}
    .st1{fill:#M8X0R8;}
    .st2{fill:url(#lg1);}
    ...
    .stN{fill:#XXXXXX;}
</style>
```
"Style" block contains style information for a document. It is organized, as shown above, for all SVG files.

---

### <p align="center" name="gradient">Gradient *(optional)*</p>

```html
<linearGradient id="lgN" gradientUnits="userSpaceOnUse" x1="86.2534" y1="6.75" x2="86.2534" y2="45.8236">
    <stop offset="0" stop-color="#I4QST2"/>
    <stop offset="0.98" stop-color="#T6CX3E"/>
</linearGradient>

<radialGradient id="lgN"gradientUnits="userSpaceOnUse" x1="35.4538" y1="1.453" x2="96.4348" y2="35.8838">
    <stop offset="0.6" stop-color="#T6CALP" />
    <stop offset="1" stop-color="#8GQSM2" />
</radialGradient>
```
"linearGradient" and "radialGradient" elements define gradients that can be applied to fill graphical elements.