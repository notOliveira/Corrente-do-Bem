document.getElementById('danger-zone').addEventListener('click', function() {
    let collapseIcon = document.getElementById('collapse-arrow');
    const dangerZone = document.getElementById('danger-zone');
    // Caso o dangerZone tenha collapsed na lista de classes, trocar a classe bi-chevron-down do collapseIcon para bi-chevron-right
    if (dangerZone.classList.contains('collapsed')) {
        collapseIcon.classList.replace('bi-chevron-down', 'bi-chevron-right');
    } else {
        collapseIcon.classList.replace('bi-chevron-right', 'bi-chevron-down');
    }
})