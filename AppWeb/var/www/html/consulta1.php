<!DOCTYPE html>
<html>
<head>
    <title>Consulta: Trofeos por Pais </title>
    <link rel="stylesheet" href="styles2.css">
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        if (!isset($_GET['mes']) || empty(trim($_GET['mes']))) {
            die("Error: No se proporcion   un mes v  lido.");
        }
        $mes = trim($_GET['mes']);

        $stmt = $pdo->prepare("
            SELECT p.nombre_pais,
                   COALESCE(SUM(tp200p.trofeos_totales), 0) + COALESCE(SUM(tp200c.trofeos_totales), 0) AS trofeos_totales
            FROM ProyectBrawlStars.Pais p
            LEFT JOIN ProyectBrawlStars.Trofeos_Pais_200_Player tp200p
                   ON p.nombre_pais = tp200p.nombre_pais AND tp200p.nombre_mes = :mes
            LEFT JOIN ProyectBrawlStars.Trofeos_Pais_200_Club tp200c
                   ON p.nombre_pais = tp200c.nombre_pais AND tp200c.nombre_mes = :mes
            GROUP BY p.nombre_pais
            ORDER BY trofeos_totales DESC;
        ");

        $stmt->execute(['mes' => $mes]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        echo "<h3>Resultados para el mes: " . htmlspecialchars($mes) . "</h3>";
        echo "<table>
                <tr>
                    <th>Pa  s</th>
                    <th>Trofeos Totales del Mes</th>
                </tr>";

        if (count($result) > 0) {
            foreach ($result as $row) {
                echo "<tr>
                        <td>" . htmlspecialchars($row['nombre_pais']) . "</td>
                        <td>" . htmlspecialchars($row['trofeos_totales']) . "</td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='2'>No se encontraron datos para el mes ingresado.</td></tr>";
        }
        echo "</table>";

    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
    <a href="index.html">Volver al Inicio</a>
</body>
</html>