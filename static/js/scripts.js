document.addEventListener('DOMContentLoaded', function() {
    const collapseAllButton = document.getElementById('collapseAll');
    const engineeringToggleButton = document.getElementById('toggle-engineering');
    const collapseElements = document.querySelectorAll('.collapse');

    // Collapse All Button (Global)
    if (collapseAllButton) {
        collapseAllButton.addEventListener('click', function() {
            let isAnySectionOpen = Array.from(collapseElements).some(element => element.classList.contains('show'));

            collapseElements.forEach(function(element) {
                let bsCollapse = new bootstrap.Collapse(element, { toggle: false });
                isAnySectionOpen ? bsCollapse.hide() : bsCollapse.show();
            });

            collapseAllButton.textContent = isAnySectionOpen ? 'Expand All' : 'Collapse All';
        });
    }

    // Engineering CV Toggle Button (Local for this card)
    if (engineeringToggleButton) {
        engineeringToggleButton.addEventListener('click', function() {
            const subSections = document.querySelectorAll('#aarhus-description, #neom-description');
            let isAnySubSectionOpen = Array.from(subSections).some(element => element.classList.contains('show'));
            const icon = engineeringToggleButton.querySelector('.toggle-icon');

            subSections.forEach(function(section) {
                let bsCollapse = new bootstrap.Collapse(section, { toggle: false });
                isAnySubSectionOpen ? bsCollapse.hide() : bsCollapse.show();
            });

            // Toggle the icon
            icon.textContent = isAnySubSectionOpen ? '+' : '-';
        });
    }
});
