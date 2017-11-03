let image = document.getElementById('image');
let magnifier = document.getElementById('magnifier');
magnifier.style.backgroundImage = 'url(' + image.src + ')';

let magnifierWidth = 300;
let magnifierHeight = 300;

magnifier.style.width = magnifierWidth + 'px';
magnifier.style.height = magnifierHeight + 'px';

document.addEventListener('mousemove', function (e) {
	let actualWidth = image.naturalWidth;
	let actualHeight = image.naturalHeight;
	let displayWidth = image.clientWidth;
	let displayHeight = image.clientHeight;

	let displayX = e.pageX - image.offsetLeft;
	let displayY = e.pageY - image.offsetTop;

	let percentWidth = displayX / displayWidth;
	let percentHeight = displayY / displayHeight;

	// position the magnifier
	let left = e.pageX - magnifierWidth / 2;
	if (left < image.offsetLeft) {
		left = image.offsetLeft;
	}
	let top = e.pageY - magnifierHeight / 2;
	if (top < image.offsetTop) {
		top = image.offsetTop;
	}
	if (left > displayWidth + image.offsetLeft - magnifierWidth) {
		left = displayWidth + image.offsetLeft - magnifierWidth;
	}
	if (top > displayHeight + image.offsetTop - magnifierHeight) {
		top = displayHeight + image.offsetTop - magnifierHeight;
	}

	magnifier.style.left = left + 'px';
	magnifier.style.top = top + 'px';

	// position the magnifier image
	let actualX = percentWidth * actualWidth;
	let actualY = percentHeight * actualHeight;
	if (actualX < magnifierWidth / 2) {
		actualX = magnifierWidth / 2;
	}
	if (actualY < magnifierHeight / 2) {
		actualY = magnifierHeight / 2;
	}
	if (actualX > actualWidth - magnifierWidth / 2) {
		actualX = actualWidth - magnifierWidth / 2;
	}
	if (actualY > actualHeight - magnifierHeight / 2) {
		actualY = actualHeight - magnifierHeight / 2;
	}

	let positionX = actualWidth - actualX + magnifierWidth / 2;
	let positionY = actualHeight - actualY + magnifierHeight / 2;

	magnifier.style.backgroundPositionX = positionX + 'px';
	magnifier.style.backgroundPositionY = positionY + 'px';
});

magnifier.addEventListener('click', function (e) {
	let actualWidth = image.naturalWidth;
	let actualHeight = image.naturalHeight;
	let displayWidth = image.clientWidth;
	let displayHeight = image.clientHeight;

	let displayX = e.pageX - image.offsetLeft;
	let displayY = e.pageY - image.offsetTop;

	let percentWidth = displayX / displayWidth;
	let percentHeight = displayY / displayHeight;

	let actualX = percentWidth * actualWidth;
	let actualY = percentHeight * actualHeight;

	console.log('click at: ' + actualX + ', ' + actualY);
});

document.addEventListener('keypress', function (e) {
	if (e.keyCode === 49) {
		image.src = 'image1.jpg';
		magnifier.style.backgroundImage = 'url(image1.jpg)';
	} else if (e.keyCode === 50) {
		image.src = 'image2.jpg';
		magnifier.style.backgroundImage = 'url(image2.jpg)';
	} else if (e.keyCode === 51) {
		image.src = 'image3.jpg';
		magnifier.style.backgroundImage = 'url(image3.jpg)';
	} else if (e.keyCode === 52) {
		image.src = 'image4.jpg';
		magnifier.style.backgroundImage = 'url(image4.jpg)';
	}
});