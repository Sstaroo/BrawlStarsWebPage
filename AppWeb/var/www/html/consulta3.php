<!DOCTYPE html>
<html>
<head>
    <title>Evoluci  n de Club</title>
    <link rel="stylesheet" href="styles2.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- Chart.js CDN -->
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        if (!isset($_GET['tag_club']) || empty(trim($_GET['tag_club']))) {
            die("Error: No se proporcion   un tag_club v  lido.");
        }

        $tag_club = trim($_GET['tag_club']);

        $stmt = $pdo->prepare("
                        SELECT
                            c.tag_club,
                            c.nombre_club,
                            e.nombre_mes,
                            e.trofeos_totales,
                            e.miembros
                        FROM
                            ProyectBrawlStars.Club c
                        JOIN (
                            SELECT DISTINCT ON (e.nombre_mes)
                                e.tag_club,
                                e.nombre_mes,
                                e.trofeos_totales,
                                e.miembros
                            FROM
                                ProyectBrawlStars.Evolucion_Club e
                            WHERE
                                e.nombre_mes IN ('February', 'March', 'August', 'September', 'October', 'November')
                                AND e.tag_club = :tag_club
                            ORDER BY
                                e.nombre_mes,
                                e.trofeos_totales ASC
                        ) e
                        ON
                            c.tag_club = e.tag_club
                        JOIN (
                            SELECT
                                'February' AS nombre_mes, 1 AS orden
                            UNION ALL SELECT
                                'March', 2
                            UNION ALL SELECT
                                'August', 3
                            UNION ALL SELECT
                                'September', 4
                            UNION ALL SELECT
                                'October', 5
                            UNION ALL SELECT
                                'November', 6
                        ) orden_meses
                        ON
                            e.nombre_mes = orden_meses.nombre_mes
                        ORDER BY
                            orden_meses.orden;

        ");
        $stmt->execute(['tag_club' => $tag_club]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (!$result) {
            die("<h3>No se encontraron datos para el tag_club ingresado.</h3><a href='index.html'>Volver al Inicio</a>");
        }

        // Mostrar resultados en tabla
        echo "<h3>Resultados para el Club: " . htmlspecialchars($tag_club) . "</h3>";
        echo "<table>
                <tr>
                    <th>Tag Club</th>
                    <th>Nombre Club</th>
                    <th>Mes</th>
                    <th>Trofeos Totales</th>
                    <th>Miembros</th>
                </tr>";
        $meses = [];
        $trofeos_totales = [];
        $miembros = [];
        foreach ($result as $row) {
            echo "<tr>
                    <td>" . htmlspecialchars($row['tag_club']) . "</td>
                    <td>" . htmlspecialchars($row['nombre_club']) . "</td>
                    <td>" . htmlspecialchars($row['nombre_mes']) . "</td>
                    <td>" . htmlspecialchars($row['trofeos_totales']) . "</td>
                    <td>" . htmlspecialchars($row['miembros']) . "</td>
                  </tr>";
            // Preparar datos para gr  ficos
            $meses[] = htmlspecialchars($row['nombre_mes']);
            $trofeos_totales[] = $row['trofeos_totales'];
            $miembros[] = $row['miembros'];
        }
        echo "</table>";

    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>

    <!-- Contenedores para gr  ficos -->
    <h3>Gr  fico de Trofeos Totales</h3>
    <canvas id="trofeosChart" width="1000" height="200"></canvas>

<h3>Gr  fico de Miembros</h3>
<canvas id="miembrosChart" width="1000" height="200"></canvas>

<a href="index.html">Volver al Inicio</a>

<script>
    // Datos de PHP a JavaScript
    const meses = <?php echo json_encode($meses); ?>;
    const trofeosTotales = <?php echo json_encode($trofeos_totales); ?>;
    const miembros = <?php echo json_encode($miembros); ?>;

    // Configuraci  n del gr  fico de Trofeos Totales
    const trofeosCtx = document.getElementById('trofeosChart').getContext('2d');
    new Chart(trofeosCtx, {
        type: 'line',
        data: {
            labels: meses,
            datasets: [{
                label: 'Trofeos Totales',
                data: trofeosTotales,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
            }
        }
    });

    // Configuraci  n del gr  fico de Miembros
        const miembrosCtx = document.getElementById('miembrosChart').getContext('2d');
        new Chart(miembrosCtx, {
            type: 'line',
            data: {
                labels: meses,
                datasets: [{
                    label: 'Miembros',
                    data: miembros,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                }
            }
        });
    </script>
</body>
</html>