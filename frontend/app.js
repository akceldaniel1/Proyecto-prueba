const { createApp } = Vue;

createApp({
    data() {
        return {
            proyectos: [],
            proyectoSeleccionado: null,
            searchTerm: '',
            cargando: false,
            error: null,
            mostrarModal: false,
            totalProyectos: 0,
            orden: {
                campo: 'id',
                direccion: 'asc'
            }
        };
    },
    mounted() {
        this.cargarProyectos();
        this.obtenerEstadisticas();
    },
    methods: {
        async cargarProyectos() {
            this.cargando = true;
            this.error = null;
            
            try {
                const response = await fetch('http://localhost:8000/proyectos/');
                if (!response.ok) {
                    throw new Error('Error al cargar los proyectos');
                }
                this.proyectos = await response.json();
                this.totalProyectos = this.proyectos.length;
            } catch (error) {
                this.error = error.message;
                console.error('Error:', error);
            } finally {
                this.cargando = false;
            }
        },
        
        async obtenerEstadisticas() {
            try {
                const response = await fetch('http://localhost:8000/proyectos/estadisticas/total');
                if (response.ok) {
                    const data = await response.json();
                    this.totalProyectos = data.total_proyectos;
                }
            } catch (error) {
                console.error('Error obteniendo estadísticas:', error);
            }
        },
        
        async buscarProyectos() {
            if (!this.searchTerm.trim()) {
                this.cargarProyectos();
                return;
            }
            
            this.cargando = true;
            this.error = null;
            
            try {
                const response = await fetch(
                    `http://localhost:8000/proyectos/buscar/${encodeURIComponent(this.searchTerm)}`
                );
                
                if (!response.ok) {
                    throw new Error('Error en la búsqueda');
                }
                
                this.proyectos = await response.json();
            } catch (error) {
                this.error = error.message;
            } finally {
                this.cargando = false;
            }
        },
        
        limpiarBusqueda() {
            this.searchTerm = '';
            this.cargarProyectos();
        },
        
        seleccionarProyecto(proyecto) {
            this.proyectoSeleccionado = proyecto;
        },
        
        async verDetalles(proyecto) {
            try {
                const response = await fetch(`http://localhost:8000/proyectos/${proyecto.id}`);
                if (response.ok) {
                    this.proyectoSeleccionado = await response.json();
                    this.mostrarModal = true;
                }
            } catch (error) {
                this.error = 'Error al cargar detalles';
                console.error('Error:', error);
            }
        },
        
        cerrarModal() {
            this.mostrarModal = false;
            this.proyectoSeleccionado = null;
        },
        
        ordenarPor(campo) {
            if (this.orden.campo === campo) {
                this.orden.direccion = this.orden.direccion === 'asc' ? 'desc' : 'asc';
            } else {
                this.orden.campo = campo;
                this.orden.direccion = 'asc';
            }
            
            this.proyectos.sort((a, b) => {
                let valorA = a[campo] || '';
                let valorB = b[campo] || '';
                
                if (typeof valorA === 'string') {
                    valorA = valorA.toLowerCase();
                    valorB = valorB.toLowerCase();
                }
                
                if (valorA < valorB) {
                    return this.orden.direccion === 'asc' ? -1 : 1;
                }
                if (valorA > valorB) {
                    return this.orden.direccion === 'asc' ? 1 : -1;
                }
                return 0;
            });
        },
        
        formatoFecha(fecha) {
            if (!fecha) return 'No especificado';
            return new Date(fecha).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },
        
        getEstadoClass(estado) {
            if (!estado) return '';
            
            const estadoLower = estado.toLowerCase();
            if (estadoLower.includes('aprob') || estadoLower.includes('finaliz')) {
                return 'estado-finalizado';
            } else if (estadoLower.includes('debate') || estadoLower.includes('discus')) {
                return 'estado-activo';
            } else {
                return 'estado-pendiente';
            }
        }
    }
}).mount('#app');