const MIN_CITIES = 2;
const MAX_CITIES = 20;

var slider = document.getElementById("speedRange")
var output = document.getElementById("output")

slider.oninput = function() {
    output.innerHTML = slider.value + " mph";
}

function generateInputs() {
    let numInputs = document.getElementById('num-inputs').value;
    const inputElement = document.getElementById('num-inputs');
    
    //ensure value stays in allowed range
    if (numInputs < MIN_CITIES) {
        numInputs = MIN_CITIES;
        inputElement.value = MIN_CITIES;
    } else if (numInputs > MAX_CITIES) {
        numInputs = MAX_CITIES;     
        inputElement.value = MAX_CITIES;
    }

    //disables buttons accordingly
    document.getElementById('decrement-btn').disabled = numInputs <= MIN_CITIES;
    document.getElementById('increment-btn').disabled = numInputs >= MAX_CITIES;
    
    const container = document.getElementById('dynamic-inputs');
    const form = document.getElementById('main-form');
    
    //saves existing inputs before clearing
    const existingValues = [];
    const currentInputs = container.querySelectorAll('input[type="text"]');
    currentInputs.forEach((input) => {
        existingValues.push(input.value.trim());
    });
    
    //clears existing inputs
    container.innerHTML = '';
    
    //adds an add button at the beginning (only if under max limit)
    if (numInputs < MAX_CITIES) {
        const addButtonContainer = document.createElement('div');
        addButtonContainer.className = 'add-button-container';
        
        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'add-btn';
        addButton.textContent = 'Add City'
        
        //add click event listener to insert a new field at the beginning
        addButton.addEventListener('click', function() {
            const currentValues = [];
            
            container.querySelectorAll('input[type="text"]').forEach((input) => {
                currentValues.push(input.value.trim());
            });
            
            currentValues.unshift('');
            
            const inputElement = document.getElementById('num-inputs');
            const newCount = Math.min(MAX_CITIES, parseInt(inputElement.value) + 1);
            inputElement.value = newCount;
            
            generateInputsWithValues(currentValues);
        });
        
        addButtonContainer.appendChild(addButton);
        container.appendChild(addButtonContainer);
    }
    
    //creates new input fields
    for (let i = 0; i < numInputs; i++) {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group';
        
        const label = document.createElement('label');
        label.textContent = `City ${i+1}:`;
        label.setAttribute('for', `input${i+1}`);
        
        const input = document.createElement('input');
        input.type = 'text';
        input.name = `input${i+1}`;
        input.id = `input${i+1}`;
        input.required = true;
        input.placeholder = `Enter city ${i+1} name`;
        
        // Restore previous value if it exists
        if (existingValues[i] !== undefined) {
            input.value = existingValues[i];
        }

        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.className = 'remove-btn';
        removeButton.textContent = 'Remove';

        //add click event listener directly to this button
        removeButton.addEventListener('click', function() {
            const inputGroups = container.querySelectorAll('.input-group');
            const currentIndex = Array.from(inputGroups).indexOf(inputGroup);
            
            const currentValues = [];
            
            //collecs all current values
            container.querySelectorAll('input[type="text"]').forEach((input) => {
                currentValues.push(input.value.trim());
            });
            

            currentValues.splice(currentIndex, 1);
            
            const inputElement = document.getElementById('num-inputs');
            inputElement.value = parseInt(inputElement.value) - 1;

            generateInputsWithValues(currentValues);
        });

        //only shows remove button if we have more than minimum inputs
        if (numInputs > MIN_CITIES) {
            inputGroup.appendChild(label);
            inputGroup.appendChild(input);
            inputGroup.appendChild(removeButton);
        } else {
            inputGroup.appendChild(label);
            inputGroup.appendChild(input);
        }

        container.appendChild(inputGroup);
        
        //adds the add button after each input group and only if under max limit
        if (numInputs < MAX_CITIES) {
            const addButtonContainer = document.createElement('div');
            addButtonContainer.className = 'add-button-container';
            
            const addButton = document.createElement('button');
            addButton.type = 'button';
            addButton.className = 'add-btn';
            addButton.textContent = 'Add City';
            
            addButton.addEventListener('click', function() {
                const inputGroups = container.querySelectorAll('.input-group');
                const insertIndex = Array.from(inputGroups).indexOf(inputGroup) + 1;
                
                const currentValues = [];
                
                container.querySelectorAll('input[type="text"]').forEach((input) => {
                    currentValues.push(input.value.trim());
                });
                
                currentValues.splice(insertIndex, 0, '');
                
                const inputElement = document.getElementById('num-inputs');
                const newCount = Math.min(MAX_CITIES, parseInt(inputElement.value) + 1);
                inputElement.value = newCount;
                
                generateInputsWithValues(currentValues);
            });
            
            addButtonContainer.appendChild(addButton);
            container.appendChild(addButtonContainer);
        }
    }
    
    form.style.display = 'block';
}

//helper function to regenerate inputs with specific values
function generateInputsWithValues(values) {
    const container = document.getElementById('dynamic-inputs');
    const form = document.getElementById('main-form');
    const numInputs = values.length;
    
    document.getElementById('decrement-btn').disabled = numInputs <= MIN_CITIES;
    document.getElementById('increment-btn').disabled = numInputs >= MAX_CITIES;

    container.innerHTML = '';
    
    //add an "Add" button at the beginning (only if under max limit)
    if (numInputs < MAX_CITIES) {
        const addButtonContainer = document.createElement('div');
        addButtonContainer.className = 'add-button-container';
        
        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'add-btn';
        addButton.textContent = 'Add City';
        
        //add click event listener to insert a new field at the beginning
        addButton.addEventListener('click', function() {
            const currentValues = [];
            
            container.querySelectorAll('input[type="text"]').forEach((input) => {
                currentValues.push(input.value.trim());
            });
            
            currentValues.unshift('');

            const inputElement = document.getElementById('num-inputs');
            const newCount = Math.min(MAX_CITIES, parseInt(inputElement.value) + 1);
            inputElement.value = newCount;
      
            generateInputsWithValues(currentValues);
        });
        
        addButtonContainer.appendChild(addButton);
        container.appendChild(addButtonContainer);
    }
    
    //creates new input fields with provided values
    for (let i = 0; i < numInputs; i++) {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group';
        
        const label = document.createElement('label');
        label.textContent = `City ${i+1}:`;
        label.setAttribute('for', `input${i+1}`);
        
        const input = document.createElement('input');
        input.type = 'text';
        input.name = `input${i+1}`;
        input.id = `input${i+1}`;
        input.required = true;
        input.placeholder = `Enter city ${i+1} name`;
        input.value = values[i] || '';

        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.className = 'remove-btn';
        removeButton.textContent = 'Remove';

        removeButton.addEventListener('click', function() {
            const inputGroups = container.querySelectorAll('.input-group');
            const currentIndex = Array.from(inputGroups).indexOf(inputGroup);
            
            const currentValues = [];
        
            container.querySelectorAll('input[type="text"]').forEach((input) => {
                currentValues.push(input.value.trim());
            });
            
            currentValues.splice(currentIndex, 1);
            
            const inputElement = document.getElementById('num-inputs');
            inputElement.value = parseInt(inputElement.value) - 1;
            
            generateInputsWithValues(currentValues);
        });

        if (numInputs > MIN_CITIES) {
            inputGroup.appendChild(label);
            inputGroup.appendChild(input);
            inputGroup.appendChild(removeButton);
        } else {
            inputGroup.appendChild(label);
            inputGroup.appendChild(input);
        }

        container.appendChild(inputGroup);
        
        if (numInputs < MAX_CITIES) {
            const addButtonContainer = document.createElement('div');
            addButtonContainer.className = 'add-button-container';
            
            const addButton = document.createElement('button');
            addButton.type = 'button';
            addButton.className = 'add-btn';
            addButton.textContent = 'Add City';
            
            
            addButton.addEventListener('click', function() {
                const inputGroups = container.querySelectorAll('.input-group');
                const insertIndex = Array.from(inputGroups).indexOf(inputGroup) + 1;
                
                const currentValues = [];
                
                container.querySelectorAll('input[type="text"]').forEach((input) => {
                    currentValues.push(input.value.trim());
                });
                
                currentValues.splice(insertIndex, 0, '');
                
                const inputElement = document.getElementById('num-inputs');
                const newCount = Math.min(MAX_CITIES, parseInt(inputElement.value) + 1);
                inputElement.value = newCount;
                
                generateInputsWithValues(currentValues);
            });
            
            addButtonContainer.appendChild(addButton);
            container.appendChild(addButtonContainer);
        }
    }
    
    form.style.display = 'block';
}


function setupEventListeners() {
    const numInputs = document.getElementById('num-inputs');
    const decrementBtn = document.getElementById('decrement-btn');
    const incrementBtn = document.getElementById('increment-btn');
    
    //when the number of inputs changes, regenerates inputs
    numInputs.addEventListener('change', generateInputs);
    
    decrementBtn.addEventListener('click', () => {
        numInputs.value = Math.max(MIN_CITIES, parseInt(numInputs.value) - 1);
        generateInputs();
    });
    
    incrementBtn.addEventListener('click', () => {
        numInputs.value = Math.min(MAX_CITIES, parseInt(numInputs.value) + 1);
        generateInputs();
    });
    
    generateInputs();
}

//initialize on load
window.addEventListener('DOMContentLoaded', setupEventListeners);