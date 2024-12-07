<!DOCTYPE html>
<html>
<head>
    <title>Top Jugadores por Trofeos</title>
    <link rel="stylesheet" href="styles2.css">
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $pdo->prepare("
            SELECT tag_jugador, MAX(nombre_pais) AS nombre_pais, MAX(trofeos_totales) AS trofeos_totales
            FROM ProyectBrawlStars.Ranking_Jugador_Pais
            WHERE puesto <= 2
            GROUP BY tag_jugador
            HAVING COUNT(DISTINCT nombre_pais) > 1;
        ");

        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        echo "<h3>Top Jugadores por Trofeos</h3>";
        echo "<table>
                <tr>
                    <th>Tag del Jugador</th>
                    <th>Pa  s</th>
                    <th>Trofeos Totales</th>
                </tr>";

        if (count($result) > 0) {
            foreach ($result as $row) {
                echo "<tr>
                        <td>" . htmlspecialchars($row['tag_jugador']) . "</td>
                        <td>" . htmlspecialchars($row['nombre_pais']) . "</td>
                        <td>" . htmlspecialchars($row['trofeos_totales']) . "</td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='3'>No se encontraron datos para los jugadores que cumplen con los criterios.</td></tr>";
        }
        echo "</table>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
    <a href="index.html">Volver al Inicio</a>
</body>
</html>