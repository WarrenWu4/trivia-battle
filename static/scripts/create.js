const categories = document.getElementById('categories');
categories.value = 'General Knowledge,';

const chips = document.querySelectorAll('.chip');
chips.forEach(chip => {
    chip.addEventListener('click', () => {
        if (chip.style.backgroundColor === 'lightgreen') {
            chip.style.backgroundColor = 'white';
            categories.value = categories.value.replace(chip.innerText + ',', ''); 
        } else {
            chip.style.backgroundColor = 'lightgreen';
            categories.value += chip.innerText + ',';
        }
        console.log(categories.value);
    });
});