<h2><p align="center"><a href="{image_path}" title="View & Download {image_name}">Pure SVG</a></p></h2>
<div class="spoiler{not_colored_image_shown}">
	<div class="spoiler_text" onclick="this.parentNode.classList.toggle('shown')"></div>
	<div class="spoiler_content">
		<div class="badges" align="center">
			<a href="{image_path}" target="_blank" title="File size">
				<img alt="File size: {image_size}" src="https://img.shields.io/static/v1?cacheSeconds=10800&style=flat&label=File%20size&message={image_size_url}&color=0aa">
			</a>
			<a href="./src/{image_compressed_path}" target="_blank" title="File size">
				<img alt="Compressed file size: {image_compressed_size}" src="https://img.shields.io/static/v1?cacheSeconds=10800&style=flat&label=Compressed&message={image_compressed_size_url}&color=bb0">
			</a>
		</div>
		<div>
			<br>
			<img src="{image_path}" alt="***There should be an image here***" title="{image_name}">
			<br>
		</div>
	</div>
</div>