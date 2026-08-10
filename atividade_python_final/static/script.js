// Modo Escuro com localStorage
const btnTheme = document.getElementById('toggleDarkMode');
if (btnTheme) {
    const themeSaved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', themeSaved);

    btnTheme.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// Filtro assíncrono (JSON / REST fetch)
const filtroSelect = document.getElementById('filtroStatus');
if (filtroSelect) {
    filtroSelect.addEventListener('change', (e) => {
        const status = e.target.value;
        fetch(`/api/tarefas?status=${status}`)
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById('listaTarefas');
                container.innerHTML = '';
                data.forEach(t => {
                    let borderClass = t.status === 'Pendente' ? 'border-warning' : (t.status === 'Em andamento' ? 'border-primary' : 'border-success');
                    let badgeClass = t.status === 'Pendente' ? 'text-bg-warning' : (t.status === 'Em andamento' ? 'text-bg-primary' : 'text-bg-success');
                    
                    container.innerHTML += `
                        <div class="col-md-4 mb-3">
                            <div class="card ${borderClass}">
                                <div class="card-body">
                                    <h5 class="card-title">${t.titulo}</h5>
                                    <p class="card-text">${t.descricao || ''}</p>
                                    <span class="badge ${badgeClass}">${t.status}</span>
                                    <div class="mt-3">
                                        <a href="/editar/${t.id}" class="btn btn-sm btn-outline-secondary"><i class="bi bi-pencil"></i></a>
                                        <a href="/excluir/${t.id}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                });
            });
    });
}