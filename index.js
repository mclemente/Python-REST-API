let selector = document.getElementById('function');
let input = document.getElementById('input');
let button = document.getElementById('button');
button.onclick = run;

function toggleInput() {
	if (selector.value == "postWhitelist") {
		input.style.display = "block";
	}
	else {
		input.style.display = "none";
	}
}
toggleInput()

async function run() {
	let response;
	switch(selector.value) {
		case "getBlacklist":
			response = await fetch('http://localhost:5000/blacklist');
			postResult(response);
			break;
		case "getWhitelist":
			response = await fetch('http://localhost:5000/whitelist');
			postResult(response);
			break;
		case "postWhitelist":
			response = await fetch('http://localhost:5000/whitelist/' + input.value, {method: 'POST'})
			break;
		case "getFilter":
			response = await fetch('http://localhost:5000/filtro');
			postResult(response);
			break
	}
}

async function postResult(response) {
	const myJson = await response.json(); //extract JSON from the http response
	document.getElementById("output").innerHTML = JSON.stringify(myJson, undefined, 2);
}