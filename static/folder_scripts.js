function main(){
	let files = document.querySelectorAll(".file");
	for (const $file of files) {
		const fileLocation = $file.getAttribute("data-location")
		$file.addEventListener("click", (ev) => {
			window.location.href = fileLocation;
		});
	}
}

window.addEventListener("load", main);