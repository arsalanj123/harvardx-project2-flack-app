function hello_on_load() {
document.addEventListener('DOMContentLoaded', function() {
    alert("hi");
})};

// Function to change heading to say goodbye
function hello() {
    document.querySelector('h1').innerHTML = 'Goodbye!';
}
