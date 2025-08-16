function updateLocationData(pincode) {
    const messageElement = document.getElementById('message');
    const cityField = document.getElementById('city');
    const districtField = document.getElementById('district');
    const stateField = document.getElementById('state');
    

    // Regular expression to validate pincode (6 digits)
    const pincodeRegex = /^[0-9]{6}$/;

    // If pincode is invalid, return early
    if (!pincode.match(pincodeRegex)) {
        messageElement.textContent = 'Please enter a valid 6-digit pincode.';
        messageElement.className = 'error';
        return;
    }
    if (pincode.match(pincodeRegex)) {
        messageElement.textContent = '';
    }

    // Show loading message while waiting for API response
    // messageElement.textContent = 'Fetching data...';
    // messageElement.className = 'loading';

    // Fetch data from the API
    fetch(`https://api.postalpincode.in/pincode/${pincode}`)
        .then(response => response.json())
        .then(data => {
            if (data[0].Status === 'Success' && data[0].PostOffice && data[0].PostOffice.length > 0) {
                const postInfo = data[0].PostOffice[0];
                const city = postInfo.Name;
                const district = postInfo.District;
                const state = postInfo.State;

                // Update the input fields with city, district, and state
                cityField.value = city;
                districtField.value = district;
                stateField.value = state;

                // Display success message
                // messageElement.textContent = 'Pincode is valid!';
                // messageElement.className = 'success';
            } else {
                console.log("Data not found");
                messageElement.textContent = 'Pincode not found or invalid.';
                messageElement.className = 'error';
            }
        })
        .catch(error => {
            messageElement.textContent = 'Error fetching data from the API.';
            messageElement.className = 'error';
            console.error('Error fetching pincode data:', error);
        });
}

// Event listener for real-time pincode validation
// document.getElementById('pincode').addEventListener('input', function() {
//     const pincode = this.value.trim();
//     updateLocationData(pincode);
// });

// --- GST VALIDATOR API ---

// Function to validate GSTIN and compare business name
// function validateGSTIN() {
//     const gstinInput = document.getElementById('gstin').value.trim(); // Get the GSTIN entered by the user
//     const companyNameInput = document.getElementById('companyName').value.trim(); // Get the business name entered by the user
//     const messageElement = document.getElementById('message1'); // Element to show the message

//     // Clear previous messages
//     messageElement.textContent = '';

//     // Regular expression to validate GSTIN format (generally 15 characters, starts with two letters)
//     const gstinRegex = /^[A-Z0-9]{15}$/;

//     // Check if the GSTIN matches the regex
//     if (!gstinRegex.test(gstinInput)) {
//         messageElement.textContent = 'Invalid GSTIN format. Please enter a valid GSTIN.';
//         messageElement.className = 'error';
//         return;
//     }

//     // Replace {api_key} with your actual API key
//     const apiKey = "3f6ec5b9bd6617bf1efd4c59d483a21d"; // Replace with your API key
//     const apiUrl = `https://sheet.gstincheck.co.in/check/${apiKey}/${gstinInput}`;
//     // x = apiUrl.response.json();
//     // console.log(x)
//     // Make the API request
//     fetch(apiUrl)
//         .then(response => response.json()) // Parse the JSON response
//         .then(data => {
//             // Check the status of the response
//             if (data.flag === true) {
//                 // If the GSTIN is found, get the company name from "lgnm"
//                 const companyName = data.data.lgnm;
//                 const tradeName = data.data.tradeNam;
//                 console.log("company name - ", companyName);
//                 console.log("trade name - ", tradeName);
                

//                 // Compare the company name fetched from the API with the user-entered business name
//                 if (companyName.toLowerCase() === companyNameInput.toLowerCase()) {
//                     // Display success message with the company name, trade name, and state
//                     // messageElement.textContent = `GSTIN is valid! Company: ${companyName}, Trade Name: ${tradeName}, State: Gujarat`;
//                     messageElement.className = 'success';
//                 } else {
//                     // If the business name doesn't match the API's company name
//                     messageElement.textContent = 'The business name does not match the GSTIN records.';
//                     messageElement.className = 'error';
//                 }
//             } else {
//                 // If the GSTIN is not found
//                 messageElement.textContent = 'GSTIN not found or invalid.';
//                 messageElement.className = 'error';
//             }
//         })
//         .catch(error => {
//             // Handle any errors that occur during the fetch
//             messageElement.textContent = 'Error validating GSTIN. Please try again later.';
//             messageElement.className = 'error';
//             console.error('Error validating GSTIN:', error);
//         });
// }

// Event listener for real-time GSTIN validation
document.getElementById("link-checkbox").addEventListener("change", function() {
    const registerButton = document.getElementById("register");
    registerButton.disabled = !this.checked;
});
// document.getElementById('gstin').addEventListener('input', validateGSTIN);
// document.getElementById('companyName').addEventListener('input', validateGSTIN);
document.getElementById('pincode').addEventListener('input', function() {
    const pincode = this.value.trim();
    updateLocationData(pincode);
});
document.querySelector('form').addEventListener('submit', function() {
    document.getElementById('district').disabled = false;
    document.getElementById('state').disabled = false;
});