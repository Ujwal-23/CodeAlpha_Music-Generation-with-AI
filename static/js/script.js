// Sample generated notes (you can update this dynamically from your backend or generate it through your Python script)
const generatedNotes = ['C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4'];

// Function to display generated notes in the HTML
function displayNotes() {
    const notesList = document.getElementById('notes-list');
    generatedNotes.forEach(note => {
        const listItem = document.createElement('li');
        listItem.textContent = note;
        notesList.appendChild(listItem);
    });
}

// Call the display function when the page loads
document.addEventListener('DOMContentLoaded', displayNotes);
