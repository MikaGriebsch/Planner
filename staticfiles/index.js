document.querySelector('.slider').addEventListener('click', () => {
    document.querySelector('.loader').style.display = 'none';
    document.querySelector('#content').style.display = 'block';
});


function updateSpan() {
    const input = document.getElementById('gradeInput').value;
    const span = document.getElementById('dynamicText');
    span.textContent = `Show time table from ${input}`;
}
