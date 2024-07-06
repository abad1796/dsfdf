import numpy as np

def run_analysis(n, m, XY_values, NC_values, BC_values, FEXT_values):
    # Convertir las listas a arrays numpy
    try:
        XY = np.array(XY_values).reshape((n, 2))
        NC = np.array(NC_values).reshape((m, 2))

        if len(BC_values) % 4 != 0:
            raise ValueError("BC_values length is not a multiple of 4")
        BC = np.array(BC_values).reshape((-1, 4))

        if len(FEXT_values) % 3 != 0:
            raise ValueError("FEXT_values length is not a multiple of 3")
        FEXT = np.array(FEXT_values).reshape((n, 3))

        # Inicialización de matrices y vectores
        K = np.zeros((2*n, 2*n))  # Matriz de rigidez global
        F = np.zeros(2*n)         # Vector de fuerzas
        d = np.zeros(2*n)         # Vector de desplazamientos

        # Agregar fuerzas externas al vector F
        for i in range(n):
            F[2*i] = FEXT[i, 0]
            F[2*i+1] = FEXT[i, 1]

        # Aplicar condiciones de frontera
        for bc in BC:
            node = bc[0]
            if bc[1] == 1:
                K[2*node, 2*node] = 1e20
            if bc[2] == 1:
                K[2*node+1, 2*node+1] = 1e20

        # Ensamblaje de la matriz de rigidez global
        for member in NC:
            node_i = member[0]
            node_j = member[1]
            xi, yi = XY[node_i]
            xj, yj = XY[node_j]
            L = np.sqrt((xj - xi)**2 + (yj - yi)**2)
            c = (xj - xi) / L
            s = (yj - yi) / L

            # Matriz de rigidez del miembro en coordenadas locales
            k_local = np.array([[ c*c,  c*s, -c*c, -c*s],
                                [ c*s,  s*s, -c*s, -s*s],
                                [-c*c, -c*s,  c*c,  c*s],
                                [-c*s, -s*s,  c*s,  s*s]])

            # Matriz de rigidez del miembro en coordenadas globales
            index = [2*node_i, 2*node_i+1, 2*node_j, 2*node_j+1]
            for ii in range(4):
                for jj in range(4):
                    K[index[ii], index[jj]] += k_local[ii, jj]

        # Resolver el sistema de ecuaciones
        d = np.linalg.solve(K, F)

        # Calcular las fuerzas internas en los miembros
        forces = []
        for member in NC:
            node_i = member[0]
            node_j = member[1]
            xi, yi = XY[node_i]
            xj, yj = XY[node_j]
            L = np.sqrt((xj - xi)**2 + (yj - yi)**2)
            c = (xj - xi) / L
            s = (yj - yi) / L

            # Vector de desplazamientos del miembro
            d_local = np.array([d[2*node_i], d[2*node_i+1], d[2*node_j], d[2*node_j+1]])

            # Fuerza interna en el miembro
            f_local = (k_local @ d_local) / L
            forces.append(f_local)

        # Resultados
        results = f"Displacements: {d}\nInternal Forces: {forces}\n"
        return results
    except Exception as e:
        raise ValueError(f"Error in data processing: {str(e)}")